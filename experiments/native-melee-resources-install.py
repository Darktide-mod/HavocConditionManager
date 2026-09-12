"""Explicit installer for an unverified local native-melee experiment.

Default is a read-only check. Every overwritten byte is backed up first.
Uninstall refuses to overwrite files changed since installation.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess

HERE=Path(__file__).resolve().parent

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def inside(root,relative):
    root=root.resolve()
    path=root/relative
    assert path.resolve().is_relative_to(root), 'Path escapes the selected directory'
    for part in (path,*path.parents):
        if part==root.parent:break
        if part.exists():
            attributes=getattr(part.stat(follow_symlinks=False),'st_file_attributes',0)
            assert not part.is_symlink() and not attributes&1024,'Links/junctions are not accepted'
    return path

def stopped():
    if os.name=='nt':
        result=subprocess.check_output(['tasklist.exe','/FI','IMAGENAME eq Darktide.exe','/FO','CSV','/NH'],
                                       creationflags=subprocess.CREATE_NO_WINDOW)
        assert b'darktide.exe' not in result.lower(),'Close Darktide before installation/removal'

def atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_name(path.name+'.hcm-native-melee-new')
    with temp.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    try:os.replace(temp,path)
    finally:
        if temp.exists():temp.unlink()

def changes(game,package_root,manifest):
    targets=[]
    bundle=inside(game,'bundle')
    for row in manifest['patches']:
        path=inside(bundle,row['file'])
        assert not path.exists(),'Patch filename occupied: '+str(path)
        targets.append((path,inside(HERE,'resources/'+row['file'])))
    database=inside(bundle,'bundle_database.data')
    assert sha(database)==manifest['source_database_sha256'],'Game resource database changed; rebuild the experiment'
    executable=inside(game,'binaries/Darktide.exe')
    assert sha(executable)==manifest['executable_sha256'],'Game executable/version differs'
    for name,expected in manifest['source_bundles'].items():
        assert sha(inside(bundle,name))==expected,'Original resource container changed: '+name
    package=inside(package_root,'starter-conditions-frenzied_assault')
    expected_files=manifest['package_files']
    if package.exists():
        for old in package.rglob('*'):
            inside(package,old.relative_to(package))
            if old.is_file():
                assert old.relative_to(package).as_posix() in expected_files,'Unexpected previous package file: '+str(old)
    for relative in expected_files:
        targets.append((inside(package,relative),inside(HERE,'package/'+relative)))
    # Commit the resource database only after its files and Lua are in place.
    targets.append((database,inside(HERE,'resources/database-experiment.data')))
    for _,source in targets:
        relative=source.relative_to(HERE).as_posix()
        assert sha(source)==manifest['payload_sha256'][relative],'Payload changed: '+relative
    return targets

def install(game,package_root,manifest,apply=False):
    stopped()
    targets=changes(game,package_root,manifest)
    if not apply:
        return dict(mode='read-only check',files=len(targets),game=str(game.resolve()),
                    package_root=str(package_root.resolve()),game_files_written=0)
    backup=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True,exist_ok=False)
    rows=[]
    for i,(target,source) in enumerate(targets):
        previous=target.exists()
        original=backup/(str(i)+'.original')
        if previous:shutil.copyfile(target,original)
        rows.append(dict(path=str(target.resolve()),backup=original.name if previous else None,
                         original_sha256=sha(original) if previous else None,new_sha256=sha(source)))
    ledger=backup/'installation.json'
    record=dict(status='prepared',rows=rows,game=str(game.resolve()),package_root=str(package_root.resolve()))
    ledger.write_text(json.dumps(record,indent=2),encoding='utf-8')
    written=[]
    try:
        for (target,source),row in zip(targets,rows):
            # Refuse changes made by another process after preflight/backup.
            assert (sha(target) if target.exists() else None)==row['original_sha256']
            atomic(target,source.read_bytes());written.append(row)
    except BaseException:
        for row in reversed(written):
            target=Path(row['path'])
            if target.exists() and sha(target)==row['new_sha256']:
                if row['backup']:atomic(target,(backup/row['backup']).read_bytes())
                else:target.unlink()
        raise
    record['status']='installed'
    ledger.write_text(json.dumps(record,indent=2),encoding='utf-8')
    return dict(mode='installed experiment',backup=str(ledger),files=len(rows),restart_required=True)

def uninstall(ledger):
    stopped()
    ledger=ledger.resolve()
    assert ledger.is_relative_to((HERE/'backups').resolve()),'Use this installer\'s own backup ledger'
    record=json.loads(ledger.read_text(encoding='utf-8'))
    assert record['status']=='installed','Backup is not a completed installation'
    manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    bundle=inside(Path(record['game']),'bundle')
    package=inside(Path(record['package_root']),'starter-conditions-frenzied_assault')
    allowed={inside(bundle,r['file']).resolve() for r in manifest['patches']}
    allowed.add(inside(bundle,'bundle_database.data').resolve())
    allowed.update(inside(package,name).resolve() for name in manifest['package_files'])
    assert len(record['rows'])==len(allowed)
    assert {Path(r['path']).resolve() for r in record['rows']}==allowed,'Backup targets differ from installer scope'
    for row in record['rows']:
        target=Path(row['path'])
        assert target.exists() and sha(target)==row['new_sha256'],'Installed file changed; refusing to overwrite: '+str(target)
        if row['backup']:
            source=inside(ledger.parent,row['backup'])
            assert sha(source)==row['original_sha256'],'Backup changed'
    # No recursive deletion. Restore only recorded files, retaining backups.
    for row in reversed(record['rows']):
        target=Path(row['path'])
        if row['backup']:atomic(target,inside(ledger.parent,row['backup']).read_bytes())
        else:target.unlink()
    record['status']='removed'
    ledger.write_text(json.dumps(record,indent=2),encoding='utf-8')
    return dict(mode='removed experiment',restored_files=len(record['rows']))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game',type=Path)
    parser.add_argument('--package-root',type=Path)
    parser.add_argument('--install',action='store_true')
    parser.add_argument('--uninstall',type=Path,metavar='BACKUP_LEDGER')
    args=parser.parse_args()
    if args.uninstall:
        assert not args.install
        result=uninstall(args.uninstall)
    else:
        assert args.game and args.package_root,'Specify --game and --package-root; default operation is read-only'
        manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
        result=install(args.game,args.package_root,manifest,args.install)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
