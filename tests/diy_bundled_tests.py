"""Real direct reads, same-ID precedence, preserved selections and frozen scripts."""
from project_env import PROJECT,CHECKS
from pathlib import Path
from lupa.luajit21 import LuaRuntime
import contextlib,json,os,shutil,tempfile
source=PROJECT/'src/HavocConditionManager/scripts/mods/HavocConditionManager/diy'
previous=os.environ.get('APPDATA');cwd=Path.cwd()
try:
 with tempfile.TemporaryDirectory(prefix='direct-packages-',dir=CHECKS) as tmp, contextlib.ExitStack() as cleanup:
  cleanup.callback(os.chdir,cwd)
  tmp=Path(tmp);(tmp/'Fatshark/Darktide').mkdir(parents=True);os.environ['APPDATA']=str(tmp)
  binaries=tmp/'game/binaries';binaries.mkdir(parents=True)
  shutil.copytree(PROJECT/'src/HavocConditionManager/diy',tmp/'game/mods/HavocConditionManager/diy')
  companion=tmp/'game/mods/HavocConditionPacks/diy'
  pack=companion/'packages/companion-example'
  shutil.copytree(PROJECT/'src/HavocConditionManager/diy/packages/starter-conditions-no_healing',pack)
  manifest=json.loads((pack/'package.json').read_text(encoding='utf-8'))
  manifest.update(id='companion-example',entry_namespace='companion-example')
  (pack/'package.json').write_text(json.dumps(manifest),encoding='utf-8')
  (companion/'index.json').write_text(json.dumps({'version':1,'packages':['companion-example']}),encoding='utf-8')
  os.chdir(binaries)
  L=LuaRuntime(unpack_returned_tuples=True)
  L.execute('Mods={lua={ffi=require("ffi"),io=io,loadstring=loadstring,debug=debug}};table.clear=function(t)for k in pairs(t)do t[k]=nil end end')
  for alias,name in [('S','schema'),('C','codec'),('K','catalog'),('F','files'),('Base','library'),('P','packages'),('H','sha256'),('PL','package_library'),('B','bundled')]:
   L.globals()[alias]=L.execute((source/('diy_'+name+'.lua')).read_text(encoding='utf8'))
  L.execute(r'''
  A=P.new(S,C,H);settings={};provider=false;reads=0
  local real_open=io.open
  Mods.lua.io={open=function(...)reads=reads+1;return real_open(...)end}
  mod={get=function(_,k)return settings[k]end,set=function(_,k,v)settings[k]=S.copy(v)end,localize=function(_,k)return k end}
  get_mod=function()return mod end
  function sources()
   local out={{name='HavocConditionManager',builtin=true,directory='builtin',files=assert(B.read(mod,'HavocConditionManager',C,P))}}
   if provider then out[#out+1]={name='HavocConditionPacks',directory='companion',files=assert(B.read(mod,'HavocConditionPacks',C,P))}end
   return out
  end
  fs=assert(F.new(require('ffi'),'HavocConditionManager'))
  local directory=assert(fs.builtin_directory('HavocConditionManager'))
  assert(directory:match('[/\\]game[/\\]mods[/\\]HavocConditionManager[/\\]diy[/\\]packages$'))
  local initial=assert(B.read(mod,'HavocConditionManager',C,P))
  assert(fs.write_package('starter-conditions-no_healing',initial['starter-conditions-no_healing'],P.id,P.path))
  local old=assert(A.validate(initial['starter-conditions-no_healing'],K,'conditions'))
  settings.diy_document_v1=assert(C.encode(A.compose({['starter-conditions-no_healing']=old},K,'conditions').document))
  local id=A.entry_identity(old,'no_healing')
  settings.diy_options_v1={enabled=true,selected={id}}
  local before=#assert(fs.list_packages(P.id))
  library=PL.new(mod,'conditions',K,S,C,F,Base,P,H,{name='HavocConditionManager',bundled=sources})
  assert(#library.files==1 and library.package_builtin('starter-conditions-no_healing'))
  assert(library.options.selected[1]==id and library.options.enabled)
  assert(not library.toggle_package('starter-conditions-no_healing'))
  assert(library.shadowed_packages['starter-conditions-no_healing'])
  assert(#assert(fs.list_packages(P.id))==before)
  local frozen=library.snapshot();local count=reads
  for i=1,1000 do assert(library.snapshot()==frozen);library.signature()end
  assert(reads==count,'No filesystem work in snapshot or gameplay signature reads')
  provider=true;assert(library.scan() and #library.files==2)
  assert(library.packages['companion-example'] and not library.package_builtin('companion-example'))
  assert(#frozen.document.entries==1 and #library.snapshot().document.entries==2)
  assert(mod._diy_native_melee_20==nil,'Discovery must not execute native condition Lua')
  assert(#assert(fs.list_packages(P.id))==before,'Companion source must not be extracted')
  assert(library.toggle_package('companion-example') and #library.document.entries==1)
  assert(library.toggle_package('companion-example') and #library.document.entries==2)
  provider=false;assert(library.scan() and #library.files==1 and library.options.selected[1]==id)
  assert(not B.read(mod,'../escape',C,P))
  ''')
finally:
 os.chdir(cwd)
 if previous is None:os.environ.pop('APPDATA',None)
 else:os.environ['APPDATA']=previous
print('PASS: direct disk reads, built-in lock, preserved selections, external shadowing, companion add/remove, zero extraction or per-frame I/O')
