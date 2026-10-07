"""Offline publishing regressions: exact ZIP, multipart bytes, receipts and retries."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
from urllib.error import HTTPError

from project_env import PROJECT, CHECKS
sys.path.insert(0, str(PROJECT / 'tools'))
from publish_nexus import Nexus, current_changelog, publish


class FakeNexus:
    def __init__(self):
        self.calls = []
        self.parts = []
        self.created = False
        self.changelog_failure = False

    def api(self, path, method='GET', body=None):
        self.calls.append((path, method, body))
        if path.startswith('/games/'):
            return dict(id='mod-global', game_scoped_id='1267', name='HavocConditionManager')
        if path == '/mods/mod-global/files':
            return {'mod_files': [dict(id='old'), *([dict(id='new')] if self.created else [])]}
        if path.endswith('/versions'):
            return {'versions': [dict(id='version-global', game_scoped_id='123', category='optional', version='4.6.0-test.3')]
                    if '/new/' in path else [dict(version='4.4.9')]}
        if path == '/uploads/multipart':
            assert body == dict(filename='HavocConditionManager-4.6.0-test.3.zip', size_bytes=9)
            return dict(id='upload', part_size_bytes=4, part_presigned_urls=['https://storage/1', 'https://storage/2', 'https://storage/3'], complete_presigned_url='https://storage/complete')
        if path == '/uploads/upload':
            return dict(state='available')
        if path == '/mod-files':
            assert not self.created
            assert body['file_category'] == 'optional'
            assert not body['primary_mod_manager_download'] and not body['update_mod_version']
            assert body['allow_mod_manager_download'] and body['show_requirements_pop_up']
            assert 'archive_existing_file' not in body
            self.created = True
            return dict(id='new', file_category='optional')
        if path.endswith('/changelogs'):
            if self.changelog_failure:
                raise RuntimeError('Submission outcome unknown')
            return {}
        raise AssertionError((path, method, body))

    def storage(self, url, method, data, content_type):
        self.parts.append((url, method, data, content_type))
        return '"etag-part"'


with tempfile.TemporaryDirectory(prefix='nexus-tests-', dir=CHECKS) as temporary:
    root = Path(temporary)
    archive = root / 'HavocConditionManager-4.6.0-test.3.zip'
    data = b'123456789'
    archive.write_bytes(data)
    plan = dict(archive=str(archive), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                version='4.6.0-test.3', current_changelog='Current changes')
    settings = dict(game_domain='warhammer40kdarktide', game_scoped_mod_id='1267', display_name='HCM test')
    receipt_path = root / 'receipt.json'
    api = FakeNexus()
    result = publish(api, settings, plan, receipt_path, wait=lambda seconds: None)
    assert result['state'] == 'complete' and result['verified_category'] == 'optional'
    assert [part[2] for part in api.parts[:3]] == [b'1234', b'5678', b'9']
    assert b'<PartNumber>3</PartNumber>' in api.parts[3][2]
    writes = len([c for c in api.calls if c[1] == 'POST'])
    publish(api, settings, plan, receipt_path, wait=lambda seconds: None)
    assert len([c for c in api.calls if c[1] == 'POST']) == writes
    assert 'storage' not in receipt_path.read_text(encoding='utf-8')

    # A lost changelog response must not cause duplicate publishing on retry.
    failed = FakeNexus()
    failed.changelog_failure = True
    journal = root / 'failed-receipt.json'
    try:
        publish(failed, settings, plan, journal, wait=lambda seconds: None)
    except RuntimeError:
        pass
    else:
        raise AssertionError('The simulated unknown changelog outcome must fail.')
    writes = len([c for c in failed.calls if c[1] == 'POST'])
    try:
        publish(failed, settings, plan, journal, wait=lambda seconds: None)
    except AssertionError as error:
        assert 'changelog' in str(error)
    else:
        raise AssertionError('An uncertain changelog must not be blindly resubmitted.')
    assert len([c for c in failed.calls if c[1] == 'POST']) == writes

    # A lost file-create response without a remote match also blocks writes.
    uncertain = dict(plan, state='creating_file', upload_id='upload')
    journal.write_text(json.dumps(uncertain), encoding='utf-8')
    fresh = FakeNexus()
    try:
        publish(fresh, settings, plan, journal, wait=lambda seconds: None)
    except AssertionError as error:
        assert 'file creation' in str(error)
    else:
        raise AssertionError('An uncertain file creation must block automatic retries.')
    assert all(call[1] == 'GET' for call in fresh.calls)

class Response:
    def __init__(self, headers=None):
        self.headers = headers or {}
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return b'{"data":{"ok":true}}'

client = Nexus('SECRET-TEST-KEY')
requests = []
def capture(request, timeout):
    requests.append(request)
    return Response({'ETag': '"part"'})
with patch.object(client.opener, 'open', capture):
    assert client.api('/test')['ok'] is True
    client.storage('https://storage.example/part?signature=private', 'PUT', b'123', 'application/octet-stream')
assert requests[0].get_header('Apikey') == 'SECRET-TEST-KEY'
assert not requests[1].get_header('Apikey')
def reject(request, timeout):
    raise HTTPError(request.full_url, 403, 'SECRET-TEST-KEY', {}, None)
with patch.object(client.opener, 'open', reject):
    try: client.api('/test', 'POST', {})
    except RuntimeError as error:
        assert '403' in str(error) and 'SECRET' not in str(error)
    else: raise AssertionError('API error must be reported without secrets.')
assert current_changelog('4.6.0-test.3\n- Current\n\n4.5.0\n- Older') == '4.6.0-test.3\n- Current'
print('Nexus publisher: multipart byte identity, optional-only settings, verified receipt, duplicate/uncertain-write guards and credential isolation: PASS')
