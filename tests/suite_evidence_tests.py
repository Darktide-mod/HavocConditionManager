"""Reject incomplete, stale and failed packaging evidence without building an archive."""
from project_env import PROJECT, CHECKS
from pathlib import Path, PurePosixPath
import ast, copy, hashlib, json, tempfile

builder=PROJECT/'tools/local_candidate.py'
tree=ast.parse(builder.read_text(encoding='utf-8-sig'))
function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='suite_evidence')
with tempfile.TemporaryDirectory(prefix='suite-evidence-',dir=CHECKS) as temporary:
    root=Path(temporary).resolve()
    assert root.is_relative_to(CHECKS.resolve())
    for path in list((PROJECT/'tests').rglob('*.py'))+[builder,PROJECT/'tools/release.py',PROJECT/'tools/archive_guard.py',PROJECT/'tools/publish_nexus.py']:
        target=root/path.relative_to(PROJECT)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
    checks=root/'build/checks';checks.mkdir(parents=True)
    runner=ast.parse((root/'tests/run.py').read_text(encoding='utf-8-sig'))
    required=next(ast.literal_eval(n.value) for n in runner.body if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='CASES' for t in n.targets))
    files={'HavocConditionManager/example.lua':b'return true\n'}
    source={name:hashlib.sha256(data).hexdigest() for name,data in files.items()}
    paths=list((root/'tests').rglob('*.py'))+[root/'tools/local_candidate.py',root/'tools/release.py',root/'tools/archive_guard.py',root/'tools/publish_nexus.py']
    inputs={path.relative_to(root).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}
    valid=dict(passed=True,selected=False,required=required,requested=required,
        results=[dict(case=case,exit_code=0) for case in required],source_payload_sha256=source,
        source_before_sha256=source,source_after_sha256=source,test_inputs_before_sha256=inputs,test_inputs_after_sha256=inputs)
    namespace=dict(ROOT=root,json=json,hashlib=hashlib)
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(builder),'exec'),namespace)
    def check(report,accepted):
        (checks/'tests-result.json').write_text(json.dumps(report),encoding='utf-8')
        try: namespace['suite_evidence'](files)
        except AssertionError:
            assert not accepted
        else: assert accepted
    check(valid,True)
    for mutation in ('selected','missing','duplicate','failed','boolean_exit','before_changed','manifest_changed','test_changed'):
        report=copy.deepcopy(valid)
        if mutation=='selected': report['selected']=True
        elif mutation=='missing': report['results'].pop()
        elif mutation=='duplicate': report['results'][-1]=report['results'][0]
        elif mutation=='failed': report['results'][0]['exit_code']=1
        elif mutation=='boolean_exit': report['results'][0]['exit_code']=False
        elif mutation=='before_changed': report['source_before_sha256']['HavocConditionManager/example.lua']='changed'
        elif mutation=='manifest_changed': report['required'].pop()
        elif mutation=='test_changed': report['test_inputs_before_sha256']['tests/run.py']='changed'
        check(report,False)
print('Packaging evidence: independent full manifest, all exit codes, source pre/post identity and test/package input freshness; 8 invalid-report cases rejected: PASS')

runtime_function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='runtime_payload')
scope=dict(MOD='HavocConditionManager',PurePosixPath=PurePosixPath,assert_no_nested_archives=lambda files:None)
exec(compile(ast.Module(body=[runtime_function],type_ignores=[]),str(builder),'exec'),scope)
required=['HavocConditionManager/HavocConditionManager.mod','HavocConditionManager/info.json',
          'HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager.lua','HavocConditionManager/diy/index.json']
extras=['HavocConditionManager/diy/packages/example/package.json','HavocConditionManager/diy/packages/example/effect.lua',
        'HavocConditionManager/THIRD_PARTY.md']
excluded=['HavocConditionManager/docs/diy/package-examples/effect.lua','HavocConditionManager/CHANGELOG.md',
          'HavocConditionManager/docs/review.json','OtherMod/scripts/example.lua','HavocConditionManager/authoring/example.json']
fixture={name:name.encode() for name in required+extras+excluded}
kept=scope['runtime_payload'](fixture)
assert set(kept)==set(required+extras) and all(kept[name]==fixture[name] for name in kept)
for name in required:
    missing=dict(fixture);missing.pop(name)
    try: scope['runtime_payload'](missing)
    except AssertionError: pass
    else: raise AssertionError('A runtime dependency was omitted: '+name)
print('Local candidate runtime policy: complete scripts/DIY plus loader/metadata/attribution; authoring docs/examples excluded, byte identity and required roots preserved: PASS')
