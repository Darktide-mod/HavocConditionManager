"""Reproduce stale MMB activity against the native presence transition method."""
import subprocess
from project_env import GAME, SOURCES
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
def native(path,cls,name,prefix=''):
    source=subprocess.run(['git','-c','gc.auto=0','-C',str(GAME),'show','HEAD:'+path],capture_output=True,check=True).stdout.decode('utf-8-sig')
    body=source.split(cls+'.'+name+' = function',1)[1].split('\nend',1)[0]
    return L.execute(prefix+'\nreturn function'+body+'\nend')
L.execute('''
local_enabled=true; realms_active=true; members=4; changes=0; sends=0
mods={HavocConditionManager={},Realms={},modular_menu_buttons={_current_state="main_menu"}}
function get_mod(name) return mods[name] end
function mods.HavocConditionManager.has_local_gameplay_authority() return local_enabled end
function mods.HavocConditionManager:hook_require(_,fn) fn(PM) end
function mods.HavocConditionManager:hook(target,name,fn)
    local original=target[name]; target[name]=function(...) return fn(original,...) end
end
PM={}; Entry={}; Settings={settings={}}
for _,id in ipairs({"training_grounds","mission","hub","loading","main_menu"}) do Settings.settings[id]={advertise_playing=false} end
-- Realms' installed evaluate_presence hook, with native activity as fallback.
function Settings.evaluate_presence(state)
    if realms_active then return state=="StateLoading" and "loading" or "training_grounds" end
    return state=="StateGameplay" and "mission" or state=="StateLoading" and "loading" or "main_menu"
end
function require() return Settings end
Managers={state={difficulty={get_parsed_havoc_data=function() return {} end}},connection={num_members=function() return members end}}
Log={info=function() changes=changes+1 end}
function table.is_empty(t) return next(t)==nil end
function Entry:set_num_mission_members(n) self._members=n end
function Entry:num_mission_members() return self._members end
function PM:_update_my_presence() sends=sends+1 end
function PM:_update_platform_presence() end
function PM:_delete_platform_presence() end
''')
entrypath='scripts/managers/presence/presence_entry_myself.lua'
L.globals().Entry.activity_id=native(entrypath,'PresenceEntryMyself','activity_id')
L.globals().Entry.set_activity_id=native(entrypath,'PresenceEntryMyself','set_activity_id')
L.globals().PM._check_activity=native('scripts/managers/presence/presence_manager.lua','PresenceManager','_check_activity','local PresenceSettings=require()')
L.execute('''
-- Same installed MMB hook. Do not change its menu spoofing in this fix.
local original=Entry.activity_id
function Entry:activity_id()
    local id=original(self)
    local menu=mods.modular_menu_buttons
    if menu and (menu._current_state=="shooting_range" or menu._current_state=="main_menu") then id="hub" end
    return id
end
me=setmetatable({_activity_id="loading"},{__index=Entry})
manager=setmetatable({_myself=me,_current_game_state_name="StateGameplay",_advertise_playing=false},{__index=PM})
for i=1,320 do manager:_check_activity() end
assert(changes==320 and sends==320,"Reproduce second-mission redundant presence sends")
''')
L.execute((SOURCES/'HavocConditionManager/scripts/mods/HavocConditionManager/presence_compat.lua').read_text(encoding='utf-8-sig'))
L.execute('''
changes=0; sends=0; me._activity_id="loading"
for i=1,320 do manager:_check_activity() end
assert(changes==1 and sends==1 and me._activity_id=="training_grounds")
assert(me:activity_id()=="hub" and mods.modular_menu_buttons._current_state=="main_menu")
manager._current_game_state_name="StateLoading"; manager:_check_activity()
assert(me._activity_id=="loading" and sends==2,"Real transitions pass through")
manager._current_game_state_name="StateGameplay"; manager:_check_activity()
assert(sends==3)
-- Matchmaking mission membership still updates normally.
realms_active=false; mods.modular_menu_buttons._current_state="mission"
manager:_check_activity(); assert(me._activity_id=="mission" and me._members==4)
members=3; manager:_check_activity(); assert(me._members==3 and sends==5)
-- Out of scope: menu, disabled HCM, remote authority and missing optional mod.
realms_active=true; mods.modular_menu_buttons._current_state="main_menu"
local_enabled=false; local before=sends
manager:_check_activity(); manager:_check_activity(); assert(sends==before+2)
local_enabled=true; manager._current_game_state_name="StateMainMenu"
manager:_check_activity(); assert(sends==before+3)
manager._current_game_state_name="StateGameplay"; mods.Realms=nil
manager:_check_activity(); assert(sends==before+4)
mods.modular_menu_buttons=nil; me._activity_id="loading"
manager:_check_activity(); assert(me._activity_id=="training_grounds")
''')
print('Presence: 320 duplicate transitions/sends reduced to one; real transitions, member updates, menu behavior, remote/disabled and optional-mod pass-through: PASS')
