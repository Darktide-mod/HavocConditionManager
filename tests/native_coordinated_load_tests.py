"""Execute the real coordinated predicates and selector for every intensity."""
from native_harness import *
L.globals().Profile=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile')
L.execute('''
local load,stage=0,"build_up_tension"
local side={valid_player_units={{},{},{},{}}}
Managers.state.pacing={state=function() return stage end,total_challenge_rating=function() return load end}
Managers.state.extension={system=function() return {get_side=function() return side end} end}
ScriptUnit={extension=function(unit) return {read_component=function() return unit end} end}
require("scripts/utilities/attack/player_unit_status").requires_help=function(c) return c.disabled end
function set_load(value) load=value;E.clear_context() end
function set_stage(value) stage=value;E.clear_context() end
function set_players(n) side.valid_player_units={};for i=1,n do side.valid_player_units[i]={} end;E.clear_context() end
function set_disabled(n) for i,u in ipairs(side.valid_player_units) do u.disabled=i<=n end;E.clear_context() end
load_checks=0;adapted_tactics=0
local supported={coordinated_special_attack=true,elite_coordinated_special_attack=true,
 elite_roamer_mix_vector=true,elite_sandwich_waves=true,sandwich=true,ranged_push_from_behind=true}
for _,entry in ipairs(A.entries) do
 if entry.family=="hordes" then
  for level=1,10 do
   local cfg=Profile.values(level)
   local compiled=S.apply(entry.root,entry.family,cfg,nil,A.breeds,A.by_table)
   for name,tactic in pairs(entry.root.coordinated_horde_strike_settings or {}) do
    local original=tactic.conditions
    local result=compiled.coordinated_horde_strike_settings[name].conditions
    if supported[name] and original and #original==3 then
     if level==1 then assert(result==original);adapted_tactics=adapted_tactics+1 end
     local maximum=35*cfg.coordinated_load
     local medium=name=="ranged_push_from_behind"
     for _,value in ipairs({0,7.99,8,34.99,35,maximum-.01,maximum,maximum+20}) do
      set_load(value)
      assert(original[3](1)==(value<35 and (not medium or value>=8)),"native slot is no longer the supported 35-point predicate: "..entry.id.."/"..name)
      assert(result[3](1)==(value<maximum and (not medium or value>=8)),entry.id.."/"..name)
      assert(Managers.state.pacing:total_challenge_rating()==value,"global threat rating changed")
      load_checks=load_checks+1
     end
     for _,value in ipairs({"build_up_tension_low","build_up_tension","build_up_tension_high","relax"}) do
      set_stage(value);assert(result[1](1)==original[1](1))
     end
     for n=1,4 do set_players(n);assert(result[2](1)==original[2](1)) end
     set_players(4);set_disabled(3);assert(not result[2](1))
     set_disabled(0);set_stage("build_up_tension")
     if name=="elite_roamer_mix_vector" then example_entry=entry;example_name=name end
    else assert(result==original,"unsupported native condition changed: "..entry.id.."/"..name) end
   end
  end
 end
end
assert(adapted_tactics>=50)
-- HED append operates on the scaled native predicates; replace remains explicit.
local target="coordinated_horde_strike_settings/"..example_name.."/conditions"
local function configure(rule)
 B.values.native_configuration_v3=Profile.values(10)
 mods.HavocEnemyDirector={is_gameplay_enabled=function() return true end,get_config=function()
  return {rules={[example_entry.id]={[target]=rule}}} end}
 Managers.state.game_session={};E.reset()
 return E.prepare(example_entry.root).coordinated_horde_strike_settings[example_name].conditions
end
local function passes(list) for _,fn in ipairs(list) do if not fn(1) then return false end end;return true end
set_load(40);set_stage("build_up_tension");set_players(4)
local conditions=configure({mode="append",match="all",clauses={{condition="load_max",value=50}}})
assert(#conditions==4 and passes(conditions))
set_load(60);assert(not passes(conditions))
conditions=configure({mode="replace",match="all",clauses={{condition="always"}}})
set_load(200);set_players(1);set_stage("relax")
assert(#conditions==1 and passes(conditions))
mods.HavocEnemyDirector=nil
''')
source=(GAME/'scripts/managers/pacing/horde_pacing/horde_pacing.lua').read_text(encoding='utf-8-sig')
start=source.index('HordePacing._evaluate_coordinated_horde_strike = function')
L.execute('local HordePacing={};local TEMP_SETTINGS={};'+source[start:source.index('\nend',start)+4]+'\nnative_evaluate=HordePacing._evaluate_coordinated_horde_strike')
L.execute('''
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.shuffle(t) return t end
local random=math.random;local draws=0
math.random=function() draws=draws+1;return .1 end
set_stage("build_up_tension");set_players(4)
for level=1,10 do
 local cfg=Profile.values(level)
 local compiled=S.apply(example_entry.root,example_entry.family,cfg,nil,A.breeds,A.by_table)
 local tactic=S.copy(compiled.coordinated_horde_strike_settings[example_name])
 tactic.chance=1;tactic.high_chance_conditions=nil
 local self={_template={coordinated_horde_strike_settings={[example_name]=tactic}},_coordinated_horde_strikes_total_num_allowed={[example_name]=1}}
 local maximum=35*cfg.coordinated_load
 set_load(maximum-.01);draws=0;assert(native_evaluate(self,1)==tactic and draws==1)
 set_load(maximum);draws=0;assert(not native_evaluate(self,1) and draws==0)
 set_load(0);set_players(1);assert(not native_evaluate(self,1))
 set_players(4);set_stage("relax");assert(not native_evaluate(self,1));set_stage("build_up_tension")
 assert(self._coordinated_horde_strikes_total_num_allowed[example_name]==1)
end
math.random=random
''')
print('All ten levels:',L.globals().adapted_tactics,'native tactics;',L.globals().load_checks,'load-boundary checks; real native selector, capable-player/stage retention, unchanged global load and HED append/replace precedence: PASS')

# Actual event dispatch still attaches recovery ownership without statistics.
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/spawn_tracking')
L.execute('function class() return {} end; function table.is_empty(t) return next(t)==nil end')
L.globals().NativeEvent=lua_file(game/'scripts/managers/event/event_manager.lua')
L.execute("""
local tracked={};local registrations,removals=0,0
function B:info() error("runtime diagnostics remain") end
ScriptUnit.has_extension=function() error("diagnostic category lookup") end
B.track_redeployed_unit=function(unit) tracked[#tracked+1]=unit end
Managers.event=setmetatable({}, {__index=NativeEvent});Managers.event:init()
function Managers.event:register(...) registrations=registrations+1;return NativeEvent.register(self,...) end
function Managers.event:unregister(...) removals=removals+1;return NativeEvent.unregister(self,...) end
host=true;B.start_spawn_tracking();B.start_spawn_tracking();assert(registrations==1)
local units={{},{},{},{},{}}
for _,u in ipairs(units) do Managers.event:trigger("minion_unit_spawned",u) end
Managers.event:trigger("minion_unit_spawned",nil)
host=false;Managers.event:trigger("minion_unit_spawned",units[1]);host=true
assert(#tracked==5)
for i,u in ipairs(units) do assert(tracked[i]==u) end
B.finish_spawn_tracking();B.finish_spawn_tracking()
assert(removals==1 and next(Managers.event._events)==nil)
Managers.event:trigger("minion_unit_spawned",units[1]);assert(#tracked==5)
B.values.native_configuration_v3=Profile.values(1);Managers.state.game_session={};E.reset()
B.start_spawn_tracking();Managers.event:trigger("minion_unit_spawned",units[1]);B.finish_spawn_tracking()
assert(#tracked==6 and registrations==2 and removals==2)
assert(not B.report_coordinated_block)
""")
print('Actual native EventManager: successful local spawns attach recovery ownership once; failed/client events ignored; reset unregisters; no diagnostic output or category scans: PASS')
