"""Publish the validated Optional Files ZIP through Nexus Mods' official v3 API.

Default mode checks the local release only. --publish uploads a new optional
file and its current changelog. Credentials come from the environment or a
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
                return json.load(response)['data']
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
        try:
            with self.opener.open(req, timeout=60) as response:
                response.read()
                return response.headers.get('ETag')
        except (HTTPError, URLError):
            raise RuntimeError('Signed storage upload failed; credential URLs are omitted from output.') from None


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
    assert config['file_category'] == 'Optional Files' and '-test.' in version
    assert config.get('runtime_only'), 'This publisher accepts only the validated runtime candidate.'
    batch = ROOT / 'release' / config['release_id']
    validate(batch, config, version, documents, payloads)
    settings = json.loads((ROOT / 'publishing/nexus.json').read_text(encoding='utf-8-sig'))
    assert settings['game_domain'] == 'warhammer40kdarktide' and settings['game_scoped_mod_id'] == '1267'
    archive = batch / f'{config["mod"]}-{version}.zip'
    plan = dict(release_id=config['release_id'], version=version, archive=str(archive),
                sha256=hashlib.sha256(archive.read_bytes()).hexdigest(), bytes=archive.stat().st_size,
                category='optional', update_mod_version=False, primary_download=False,
                page=f'https://www.nexusmods.com/{settings["game_domain"]}/mods/{settings["game_scoped_mod_id"]}?tab=files',
                current_changelog=current_changelog(documents['changelog.en.txt']))
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


def publish(api, settings, plan, receipt_path, wait=time.sleep):
    assert hashlib.sha256(Path(plan['archive']).read_bytes()).hexdigest() == plan['sha256'], 'The archive changed after validation.'
    mod = api.api(f'/games/{settings["game_domain"]}/mods/{settings["game_scoped_mod_id"]}')
    assert str(mod['game_scoped_id']) == settings['game_scoped_mod_id'] and mod.get('name') == 'HavocConditionManager'
    mod_id = str(mod['id'])
    receipt = json.loads(receipt_path.read_text(encoding='utf-8')) if receipt_path.exists() else dict(plan)
    assert receipt['sha256'] == plan['sha256'] and receipt['version'] == plan['version']
    existing = existing_version(api, mod_id, plan['version'])
    if existing:
        assert existing['category'] == 'optional', 'The existing version has an unexpected category.'
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
        receipt['state'] = 'creating_file'
        save_receipt(receipt_path, receipt)
        created = api.api('/mod-files', 'POST', dict(upload_id=receipt['upload_id'], mod_id=mod_id,
            name=settings['display_name'], version=plan['version'], description=plan['current_changelog'],
            file_category='optional', primary_mod_manager_download=False,
            allow_mod_manager_download=True, show_requirements_pop_up=True, update_mod_version=False))
        assert created['file_category'] == 'optional'
        receipt.update(state='file_created', file_id=created['id'])
        save_receipt(receipt_path, receipt)
        existing = existing_version(api, mod_id, plan['version'])
        assert existing and existing['category'] == 'optional', 'The created file has not been verified on Nexus.'
        receipt.update(file_version_id=existing['id'], game_scoped_file_id=existing['game_scoped_id'])
        save_receipt(receipt_path, receipt)
    if not receipt.get('changelog_added'):
        assert not receipt.get('changelog_pending'), 'A previous changelog submission has an unknown outcome; inspect it before retrying.'
        receipt['changelog_pending'] = True
        save_receipt(receipt_path, receipt)
        api.api(f'/mods/{quote(mod_id, safe="")}/changelogs', 'POST', dict(version=plan['version'], changelog=plan['current_changelog']))
        receipt.update(changelog_added=True, changelog_pending=False)
    receipt.update(state='complete', verified_category='optional', virus_scan_verdict='not asserted')
    save_receipt(receipt_path, receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--key-file', type=Path, default=KEY_FILE)
    args = parser.parse_args()
    settings, plan = local_release()
    if not args.publish:
        print(json.dumps(dict(plan, status='local validation passed; no network requests'), indent=2))
        return
    receipt_path = ROOT / 'build/nexus' / plan['release_id'] / 'receipt.json'
    result = publish(Nexus(read_key(args.key_file)), settings, plan, receipt_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
