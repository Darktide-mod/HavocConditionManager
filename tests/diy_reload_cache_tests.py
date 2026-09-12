"""Explicit refresh cache boundaries and late asynchronous resource callbacks."""
from project_env import PROJECT
from lupa.luajit21 import LuaRuntime
root=PROJECT/'src/HavocConditionManager/scripts/mods/HavocConditionManager'
L=LuaRuntime(unpack_returned_tuples=True)
L.globals().Assets=L.execute((root/'diy/diy_assets.lua').read_text(encoding='utf-8'))
L.globals().Hash=L.execute((root/'diy/diy_sha256.lua').read_text(encoding='utf-8'))
L.execute(r'''
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
local requests={};local provider={get_resource_name=function()end,load_animation=function()end}
provider.load_texture=function(path)
    local promise={};function promise:next(ok,failed)self.ok,self.failed=ok,failed end
    requests[#requests+1]=promise;return promise
end
local manager=Assets.new({is_enabled=function()return true end},Hash,{provider=function()return provider end})
local pack={manifest={id='cache-test',assets={{id='icon',type='texture',path='resources/icon.png'}}},asset_base='owned-test-path'}
local delivered=0;local scope=assert(manager.open(pack));local old=scope:load('icon',function()delivered=delivered+1 end)
assert(manager.status().pending==1)
manager.clear_cache();assert(old:status()=='cancelled')
assert(manager.status().records==0 and manager.status().scopes==0)
local fresh_scope=assert(manager.open(pack));local fresh=fresh_scope:load('icon',function()delivered=delivered+1 end)
assert(#requests==2 and manager.status().records==1)
requests[1].failed('old request failed');requests[1].ok({is_ok=true,resource_name='old'})
assert(manager.status().records==1 and manager.status().pending==1 and delivered==0,'Late old callbacks cannot corrupt the new cache')
requests[2].ok({is_ok=true,resource_name='new',texture='new_texture'})
assert(fresh:get().resource_name=='new' and delivered==1)
manager.clear_cache();manager.clear_cache();assert(manager.status().records==0 and fresh:status()=='cancelled')
''')
# Execute real HCM wiring with isolated providers. Library file I/O and real
# package/module generations are covered separately by package_reload_tests.
L.globals().wiring=(root/'diy_conditions.lua').read_text(encoding='utf-8')
L.execute(r'''
local busy=false;local events={};local engines={};local reload_options
local function event(name)events[#events+1]=name end
local native={finish=function()event('native_finish')end,invalidate=function()event('invalidate')end,update=function()end}
local assets={close_all=function()event('close_assets')end,clear_cache=function()event('clear_assets')end,update=function()end,status=function()return {}end}
local library={snapshot=function()return {options={enabled=true},document={entries={{}}}}end,runtime_error=function()end}
local modules={
    diy_schema={},diy_codec={},diy_catalog={},diy_library={},diy_files={},diy_network={new=function()return {finish=function()event('network_finish')end,update=function()end}end},
    diy_packages={new=function()return {}end},diy_sha256={},diy_assets={new=function()return assets end},
    diy_seed={new=function()return {resolve=function()return 42 end}end},
    diy_package_library={new=function(_,_,_,_,_,_,_,_,_,options)reload_options=options;return library end},
    diy_game={new=function()return native end},diy_scripts={attach=function(e)return e end},
    diy_engine={choose=function()return {}end,new=function()
        local e={set_global=function()end,tick=function()end,active_ids=function()return {}end,effects=function()return {}end}
        function e.finish()e.finished=true;event('finish_engine')end
        engines[#engines+1]=e;return e
    end},
}
local mod={has_local_gameplay_authority=function()return true end,hook=function()end,localize=function()return 'test' end}
function mod:io_dofile(path)return assert(modules[path:match('([^/]+)$')],path)end
get_mod=function()return mod end;require=function()return {}end
Managers={state={game_session={},game_mode={game_mode_name=function()return busy and 'mission' or 'hub' end}}}
assert(assert(loadstring(wiring))())
busy=true;mod.update_diy_conditions(.1);assert(#engines==1)
events={};reload_options.before_reload()
assert(#events==1 and events[1]=='invalidate' and not engines[1].finished,'Mid-mission refresh only invalidates derived effect reads')
busy=false;events={};reload_options.before_reload()
assert(table.concat(events,',')=='finish_engine,close_assets,clear_assets,invalidate','Finish active closures before clearing resources and loading the next package')
assert(engines[1].finished)
busy=true;mod.update_diy_conditions(.1);assert(#engines==2 and not engines[2].finished)
mod.finish_diy_conditions();assert(engines[2].finished)
''')
print('PASS: refresh clears parsed snapshots and idle runtime/resource caches before reload; active mission remains frozen; cleanup order, fresh next mission and old resource callback isolation verified.')
