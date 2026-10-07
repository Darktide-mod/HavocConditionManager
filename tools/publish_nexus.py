"""Publish the validated release ZIP through Nexus Mods' official v3 API.

Default mode checks the local release only. --publish uploads the configured
release, current changelog and page text. Credentials come from the environment or a
local config file outside the repository; no browser session is required.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from xml.sax.saxutils import escape

from release import ROOT, collect_sources, validate

API = 'https://api.nexusmods.com/v3'
KEY_FILE = Path.home() / '.config/nexusmods/HCM.env'


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Nexus:
    def __init__(self, key):
        self.key = key
        self.opener = build_opener(NoRedirect())

    def api(self, path, method='GET', body=None):
        assert path.startswith('/') and not urlsplit(path).netloc
        data = None if body is None else json.dumps(body).encode('utf-8')
        req = Request(API + path, data=data, method=method, headers={
            'apikey': self.key, 'Content-Type': 'application/json',
            'Accept': 'application/json', 'User-Agent': 'HavocConditionManager/NexusPublisher'})
        try:
            with self.opener.open(req, timeout=45) as response:
                if response.status == 204:
                    return {}
                payload = json.load(response)
                # Bulk moves return their documented result without a data envelope.
                if path == '/mod-file-versions/move':
                    assert 'versions' in payload and 'target_mod_file' in payload
                    return payload
                return payload['data']
        except HTTPError as error:
            raise RuntimeError(f'Nexus {method} {path}: HTTP {error.code}; no automatic retry of writes.') from None
        except URLError:
            raise RuntimeError(f'Nexus {method} {path}: connection failed; write outcome may be unknown.') from None

    def storage(self, url, method, data, content_type):
        # Signed storage requests deliberately carry no Nexus API key.
        parts = urlsplit(url)
        assert parts.scheme == 'https' and parts.hostname and not parts.username and not parts.password
        req = Request(url, data=data, method=method, headers={
            'Content-Type': content_type, 'Content-Length': str(len(data))})
        for attempt in range(3 if method == 'PUT' else 1):
            try:
                with self.opener.open(req, timeout=60) as response:
                    response.read()
                    return response.headers.get('ETag')
            except HTTPError as error:
                reason = f'HTTP {error.code}'
                retryable = error.code in (408, 429, 500, 502, 503, 504)
            except URLError as error:
                reason = 'connection error (' + type(error.reason).__name__ + ')'
                retryable = True
            if method != 'PUT' or not retryable or attempt == 2:
                raise RuntimeError(f'Signed storage {method} failed: {reason}; credential URLs omitted.') from None
            # Repeating the same part PUT is idempotent; completion POSTs are not retried.
            print('Retrying the same storage part:', reason, flush=True)
            time.sleep(2 * (attempt + 1))


def read_key(path=KEY_FILE):
    key = os.environ.get('NEXUSMODS_API_KEY', '').strip()
    if not key and path.is_file():
        assert not path.resolve().is_relative_to(ROOT.resolve()), 'Keep the key file outside the repository.'
        values = [line.split('=', 1)[1].strip().strip('"\'') for line in path.read_text(encoding='utf-8-sig').splitlines()
                  if line.strip().startswith('NEXUSMODS_API_KEY=')]
        assert len(values) == 1, 'The local config needs exactly one NEXUSMODS_API_KEY entry.'
        key = values[0]
    if not key:
        raise RuntimeError('Nexus API key is missing. Set NEXUSMODS_API_KEY or fill the local HCM.env file.')
    return key


def current_changelog(text):
    return text.strip().split('\n\n', 1)[0]


def local_release():
    config, version, documents, payloads = collect_sources()
    assert config.get('runtime_only'), 'This publisher accepts only the validated runtime candidate.'
    category = 'main' if config['file_category'] == 'Main Files' else 'optional'
    assert ('-test.' in version) == (category == 'optional')
    batch = ROOT / 'release' / config['release_id']
    validate(batch, config, version, documents, payloads)
    settings = json.loads((ROOT / 'publishing/nexus.json').read_text(encoding='utf-8-sig'))
    assert settings['game_domain'] == 'warhammer40kdarktide' and settings['game_scoped_mod_id'] == '1267'
    archive = batch / f'{config["mod"]}-{version}.zip'
    plan = dict(release_id=config['release_id'], version=version, archive=str(archive),
                sha256=hashlib.sha256(archive.read_bytes()).hexdigest(), bytes=archive.stat().st_size,
                category=category, update_mod_version=category == 'main', primary_download=category == 'main',
                page=f'https://www.nexusmods.com/{settings["game_domain"]}/mods/{settings["game_scoped_mod_id"]}?tab=files',
                current_changelog=current_changelog(documents['changelog.en.txt']))
    chinese_summary = (ROOT / 'publishing/summary.zh-CN.txt').read_text(encoding='utf-8-sig').strip()
    plan.update(summary=documents['summary.en.txt'].strip() + ' ' + chinese_summary,
                description=documents['description.bbcode.txt'].strip())
    assert len(plan['summary']) <= 350 and chinese_summary
    if category == 'main':
        assert settings['replace_file_id'] and settings['previous_version_id']
        plan.update(replace_file_id=settings['replace_file_id'], previous_version_id=settings['previous_version_id'])
    return settings, plan


def existing_version(api, mod_id, version):
    files = api.api(f'/mods/{quote(mod_id, safe="")}/files')['mod_files']
    found = []
    for file in files:
        versions = api.api(f'/mod-files/{quote(file["id"], safe="")}/versions')['versions']
        found.extend(item for item in versions if item['version'] == version)
    assert len(found) <= 1, 'More than one matching remote version exists; inspect Nexus before uploading.'
    return found[0] if found else None


def save_receipt(path, receipt):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def merge_previous_versions(api, mod_id, settings, plan):
    wanted = settings.get('merge_previous_version_ids', [])
    if not wanted:
        return
    all_versions = []
    for file in api.api(f'/mods/{mod_id}/files')['mod_files']:
        all_versions.extend(api.api(f'/mod-files/{file["id"]}/versions')['versions'])
    indexed = {version['id']: version for version in all_versions}
    assert all(version_id in indexed for version_id in wanted), 'Only this mod\'s earlier versions may be moved.'
    target = indexed[plan['previous_version_id']]
    assert target['file']['id'] == plan['replace_file_id']
    pending = [version_id for version_id in wanted if indexed[version_id]['file']['id'] != plan['replace_file_id']]
    if pending:
        api.api('/mod-file-versions/move', 'POST', dict(version_ids=pending,
            target=dict(target_version_id=plan['previous_version_id'], relative_placement='after')))
    for version_id in wanted:
        assert api.api(f'/mod-file-versions/{version_id}')['file']['id'] == plan['replace_file_id']


def publish(api, settings, plan, receipt_path, wait=time.sleep):
    assert hashlib.sha256(Path(plan['archive']).read_bytes()).hexdigest() == plan['sha256'], 'The archive changed after validation.'
    mod = api.api(f'/games/{settings["game_domain"]}/mods/{settings["game_scoped_mod_id"]}')
    assert str(mod['game_scoped_id']) == settings['game_scoped_mod_id'] and mod.get('name') == 'HavocConditionManager'
    mod_id = str(mod['id'])
    receipt = json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else dict(plan)
    assert receipt['sha256'] == plan['sha256'] and receipt['version'] == plan['version']
    category = plan.get('category', 'optional')
    assert category in ('main', 'optional')
    existing = existing_version(api, mod_id, plan['version'])
    if existing:
        assert existing['category'] == category, 'The existing version has an unexpected category.'
        receipt.update(state='file_created', file_version_id=existing['id'], game_scoped_file_id=existing['game_scoped_id'])
        save_receipt(receipt_path, receipt)
    else:
        assert receipt.get('state') not in ('creating_file', 'file_created', 'complete'), 'An earlier file creation may have succeeded; verify its outcome before retrying.'
        if not receipt.get('upload_id'):
            upload = api.api('/uploads/multipart', 'POST', dict(filename=Path(plan['archive']).name, size_bytes=plan['bytes']))
            receipt.update(state='uploading', upload_id=upload['id'])
            save_receipt(receipt_path, receipt)
            size = int(upload['part_size_bytes'])
            assert size > 0 and len(upload['part_presigned_urls']) == math.ceil(plan['bytes'] / size)
            parts = []
            uploaded_hash = hashlib.sha256()
            with Path(plan['archive']).open('rb') as archive:
                for number, url in enumerate(upload['part_presigned_urls'], 1):
                    chunk = archive.read(size)
                    uploaded_hash.update(chunk)
                    etag = api.storage(url, 'PUT', chunk, 'application/octet-stream')
                    assert etag, 'Storage did not return an ETag.'
                    parts.append(f'<Part><PartNumber>{number}</PartNumber><ETag>{escape(etag.strip(chr(34)))}</ETag></Part>')
                assert not archive.read(1)
            assert uploaded_hash.hexdigest() == plan['sha256'], 'Uploaded parts differ from the validated ZIP.'
            xml = ('<CompleteMultipartUpload>' + ''.join(parts) + '</CompleteMultipartUpload>').encode('utf-8')
            api.storage(upload['complete_presigned_url'], 'POST', xml, 'application/xml')
            receipt['state'] = 'uploaded'
            save_receipt(receipt_path, receipt)
        assert receipt['state'] in ('uploaded', 'finalising', 'available'), 'An incomplete multipart upload cannot be blindly retried.'
        upload_path = f'/uploads/{quote(receipt["upload_id"], safe="")}'
        upload = api.api(upload_path)
        if upload['state'] != 'available':
            receipt['state'] = 'finalising'
            save_receipt(receipt_path, receipt)
            api.api(upload_path + '/finalise', 'POST')
        for attempt in range(20):
            upload = api.api(upload_path)
            if upload['state'] == 'available':
                break
            print('Nexus upload processing:', upload['state'], flush=True)
            wait(min(2 * 1.5 ** attempt, 15))
        else:
            raise RuntimeError('Nexus is still processing this upload. The receipt preserves its ID for a later retry.')
        if category == 'main':
            merge_previous_versions(api, mod_id, settings, plan)
        receipt['state'] = 'creating_file'
        save_receipt(receipt_path, receipt)
        body = dict(upload_id=receipt['upload_id'],
            name=settings['display_name'], version=plan['version'], description=plan['current_changelog'],
            file_category=category, primary_mod_manager_download=category == 'main',
            allow_mod_manager_download=True, show_requirements_pop_up=True, update_mod_version=category == 'main')
        if category == 'main':
            body.update(archive_existing_file=True, previous_version_id=plan['previous_version_id'])
            created = api.api(f'/mod-files/{plan["replace_file_id"]}/versions', 'POST', body)['file']
        else:
            body['mod_id'] = mod_id
            created = api.api('/mod-files', 'POST', body)
        assert created['file_category'] == category
        receipt.update(state='file_created', file_id=created['id'])
        save_receipt(receipt_path, receipt)
        existing = existing_version(api, mod_id, plan['version'])
        assert existing and existing['category'] == category, 'The created file has not been verified on Nexus.'
        if category == 'main': assert existing.get('is_primary') is True
        receipt.update(file_version_id=existing['id'], game_scoped_file_id=existing['game_scoped_id'])
        save_receipt(receipt_path, receipt)
    if not receipt.get('changelog_added'):
        assert not receipt.get('changelog_pending'), 'A previous changelog submission has an unknown outcome; inspect it before retrying.'
        receipt['changelog_pending'] = True
        save_receipt(receipt_path, receipt)
        api.api(f'/mods/{quote(mod_id, safe="")}/changelogs', 'POST', dict(version=plan['version'], changelog=plan['current_changelog']))
        receipt.update(changelog_added=True, changelog_pending=False)
    if plan.get('description'):
        page_hash = hashlib.sha256((plan['summary'] + '\n' + plan['description']).encode('utf-8')).hexdigest()
        if receipt.get('page_text_sha256') != page_hash:
            api.api(f'/mods/{mod_id}', 'PATCH', dict(summary=plan['summary'], description=plan['description']))
            receipt.update(page_synced=True, page_text_sha256=page_hash)
    receipt.update(state='complete', verified_category=category, virus_scan_verdict='not asserted')
    save_receipt(receipt_path, receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--key-file', type=Path, default=KEY_FILE)
    args = parser.parse_args()
    settings, plan = local_release()
    if not args.publish:
        visible = {key: value for key, value in plan.items() if key != 'description'}
        print(json.dumps(dict(visible, description_characters=len(plan['description']), status='local validation passed; no network requests'), indent=2))
        return
    receipt_path = ROOT / 'build/nexus' / plan['release_id'] / 'receipt.json'
    result = publish(Nexus(read_key(args.key_file)), settings, plan, receipt_path)
    print(json.dumps({key: value for key, value in result.items() if key != 'description'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
