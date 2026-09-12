"""Formal source and stripped payload contain no retired diagnostic/generator code."""
import sys,re,json
from pathlib import Path
from project_env import PROJECT
from lupa.luajit21 import LuaRuntime
sys.path.insert(0,str(PROJECT/'tools'))
from strip_debug import payloads,without_package_log_adapter,PACKAGE_LOG_ADAPTER,PACKAGE_FACTORY
from release import collect_sources
files={p.relative_to(PROJECT/'src').as_posix():p.read_bytes() for p in (PROJECT/'src').rglob('*') if p.is_file()}
normal=payloads(files); clean=payloads(files,True)
assert set(normal)==set(clean), "Formal source already excludes diagnostic modules"
retired={"performance_stats.lua","comparison_debug.lua","capacity_stats.lua","reference_conditions.lua","auric_conditions.lua","native_spawn.lua","native_scaling.lua","spawn_queue.lua","planner.lua","runtime.lua","buff_capacity.lua","population.lua","native_specials.lua","encounter_reporting.lua"}
for name in clean: assert Path(name).name not in retired,name
lua=LuaRuntime(unpack_returned_tuples=True)
compile_lua=lua.eval('function(s,n) local f,e=loadstring(s,n);return f~=nil,e end')
for name,data in clean.items():
    if not name.endswith(('.lua','.mod')): continue
    text=data.decode('utf-8-sig');ok,error=compile_lua(text,name);assert ok,(name,error)
    checked=without_package_log_adapter(name,text)
    for token in ('PERF_DEBUG','performance_debug','comparison_debug','ComparePerf','Perf.','capacity_stats','spawn_generation_mode','buff_capacity',':info(',':debug(',':dump(', 'debug_evidence','Placement receipt','Recovery debug','Spawn batch receipt','report_coordinated_block','doors_usable','route_links','door_rechecks'):
        assert token not in checked,(name,token)
    for target in re.findall(r'io_dofile\(\s*"([^"]+)"',text):
        if target.split('/')[0]==PROJECT.name: assert target+'.lua' in clean,(name,target)
config,version,documents,built=collect_sources()
is_test='-test.' in version
assert config['file_category']==('Optional Files' if is_test else 'Main Files')
if not is_test: assert config['diagnostics_stripped']
assert re.fullmatch(re.escape(version)+r'(?:-r[0-9]+)?',config['release_id'])
assert built==(normal if is_test else clean) and not documents['changelog.en.txt'].startswith('Packaging variant:')
assert 'comparison_debug_build' not in json.loads(clean[PROJECT.name+'/info.json'])
assert PACKAGE_LOG_ADAPTER in clean[PACKAGE_FACTORY].decode('utf-8')
for name,text in [(PACKAGE_FACTORY,'mod:info("unexpected automatic output")'),('unexpected.lua',PACKAGE_LOG_ADAPTER),
                  (PACKAGE_FACTORY,PACKAGE_LOG_ADAPTER+'\nmod:debug("unexpected")')]:
    try: payloads({name:text.encode('utf-8')},True)
    except AssertionError: pass
    else: raise AssertionError('Unrelated diagnostic output must still be rejected')
print('Source and payload: no retired diagnostic modules; all Lua compiles, imports resolve, release category/version and changelog are consistent: PASS')
