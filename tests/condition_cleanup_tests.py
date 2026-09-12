"""Native stimmed-minion listener survives native deactivation; scoped cleanup."""
import re, subprocess
from project_env import GAME, SOURCES
from lupa.luajit21 import LuaRuntime

L=LuaRuntime(unpack_returned_tuples=True)
def native(path):
    p=GAME/path
    return p.read_text(encoding='utf-8-sig') if p.is_file() else subprocess.check_output(
        ['git','-c','gc.auto=0','show','HEAD:'+path],cwd=GAME).decode('utf-8-sig')
def install(path, cls, *names):
    source=native(path)
    for name in names:
        body=re.search(r'^'+cls+r'\.'+name+r' = function\b.*?^end$',source,re.M|re.S)
        assert body, (cls,name)
        L.execute(body.group(0))

L.execute('''
function table.is_empty(t) return next(t)==nil end
MutatorManager={};MutatorStimmedMinions={};MutatorBase={};EventManager={}
MutatorStimmedMinions.super={init=function(self,server,_,template)
 self._is_server=server;self._template=template
end}
function MutatorStimmedMinions:new(server,_,template)
 local obj=setmetatable({}, {__index=self});obj:init(server,nil,template);return obj
end
function MutatorStimmedMinions:_remove_event_listeners() end
function MutatorStimmedMinions:_remove_buffs() end
Templates={stim={mutators={"stim"}},duplicate={mutators={"stim"}}}
MutatorTemplates={stim={class="scripts/managers/mutator/mutators/mutator_stimmed_minions",breed_chances={},activate_on_load=false}}
function require(path)
 if path=="scripts/settings/circumstance/circumstance_templates" then return Templates end
 if path=="scripts/managers/mutator/mutator_manager" then return MutatorManager end
 if path==MutatorTemplates.stim.class then return MutatorStimmedMinions end
 return {}
end
active=true
local data={circumstances={"stim","duplicate"}}
Managers={state={difficulty={get_parsed_havoc_data=function() return data end}}}
mod={has_local_gameplay_authority=function() return active end}
function get_mod() return mod end
function mod:hook(target,name,fn)
 local raw=target[name];target[name]=function(...) return fn(raw,...) end
end
function mod:hook_safe(target,name,fn)
 local raw=target[name];target[name]=function(...) raw(...);fn(...) end
end
Log={warning=function() error("Unexpected duplicate mutator") end}
''')
install('scripts/managers/event/event_manager.lua','EventManager','register','unregister')
install('scripts/managers/mutator/mutators/mutator_stimmed_minions.lua',
        'MutatorStimmedMinions','init','destroy')
install('scripts/managers/mutator/mutators/mutator_base.lua','MutatorBase','deactivate')
install('scripts/managers/mutator/mutator_manager.lua','MutatorManager',
        'load_mutator_from_name','deactivate_mutator','destroy')
L.execute('''
MutatorStimmedMinions.deactivate=MutatorBase.deactivate
function new_events() return setmetatable({_events={},_callbacks={}}, {__index=EventManager}) end
function new_manager(server)
 return setmetatable({_mutators={},_is_server=server},{__index=MutatorManager})
end
Managers.event=new_events()
local original=new_manager(true)
local stim=original:load_mutator_from_name("stim");stim._is_active=true
original:destroy()
assert(Managers.event._events.minion_aggroed[stim],"native teardown reproduces leaked listener")
stim:destroy();assert(not Managers.event._events.minion_aggroed)
''')
source=SOURCES/'HavocConditionManager/scripts/mods/HavocConditionManager/condition_compatibility.lua'
L.execute(source.read_text(encoding='utf-8-sig'))
L.execute('''
-- Own events are cleaned even after authority and global event ownership change.
for pass=1,3 do
 active=true; Managers.event=new_events();local events=Managers.event
 local foreign={};events:register(foreign,"minion_aggroed","foreign_callback")
 local owner=new_manager(true);owner:_load_mutators("default")
 local stim=owner._mutators.stim;stim._is_active=true
 assert(events._events.minion_aggroed[stim] and owner._hcm_aggro_listeners[stim]==events)
 Managers.state.mutator=owner
 active=false
 if pass==2 then
  -- GameplayStateRun exit executes before a deferred DMF disable removes hooks.
  mod.cleanup_condition_listeners();mod.cleanup_condition_listeners()
  assert(not events._events.minion_aggroed[stim])
 end
 if pass==3 then
  -- Explicit native unloading may already have removed this listener.
  stim:destroy();owner._mutators.stim=nil
 end
 Managers.event=new_events()
 owner:destroy()
 assert(not events._events.minion_aggroed[stim] and not owner._hcm_aggro_listeners)
 assert(events._events.minion_aggroed[foreign]=="foreign_callback")
end
-- A guest registers no host-side listener; another manager is untouched.
active=true;Managers.event=new_events()
local guest=new_manager(false);guest:_load_mutators("default");guest:destroy()
assert(not Managers.event._events.minion_aggroed and not guest._hcm_aggro_listeners)
local foreign=new_manager(true);local stim=foreign:load_mutator_from_name("stim")
foreign:destroy();assert(Managers.event._events.minion_aggroed[stim])
''')
main=(source.parent/'HavocConditionManager.lua').read_text(encoding='utf-8-sig')
exit_handler=main.split('mod.on_game_state_changed=function',1)[1]
assert exit_handler.index('mod.cleanup_condition_listeners()') < exit_handler.index('toggle.finish()')
print('Native aggro listener leak reproduced; own server cleanup, authority loss, repeat missions, deferred disable, prior removal and unrelated listeners: PASS')
