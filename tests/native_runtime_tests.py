"""Execute the game's native consumers across the new hooks."""
from native_harness import *

def method(path,owner,name,prefix=""):
    text=(GAME/path).read_text(encoding="utf-8-sig")
    start=text.index(owner+"."+name+" = function")
    end=text.index("\nend",start)+len("\nend")
    return L.execute(prefix+"\n"+text[start:end]+"\nreturn "+owner+"."+name)
L.execute("function table.clear(t) for k in pairs(t) do t[k]=nil end end; function table.shuffle(t) return t end; Log={info=function() end}; NativeSpecial={}; NativeHorde={}; NativeTerror={}; NativeAuto={}")
cache["scripts/utilities/loaded_dice"]=lua_file(GAME/"scripts/utilities/loaded_dice.lua")
load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks")
L.globals().native_special_setup=method("scripts/managers/pacing/specials_pacing/specials_pacing.lua","SpecialsPacing","_setup","local SpecialsPacing=NativeSpecial")
L.globals().native_horde_init=method("scripts/managers/pacing/horde_pacing/horde_pacing.lua","HordePacing","_init_coordinated_horde_strikes","local HordePacing=NativeHorde")
L.globals().native_horde_evaluate=method("scripts/managers/pacing/horde_pacing/horde_pacing.lua","HordePacing","_evaluate_coordinated_horde_strike","local HordePacing=NativeHorde; local TEMP_SETTINGS={}")
L.globals().native_horde_allowance=method("scripts/managers/pacing/horde_pacing/horde_pacing.lua","HordePacing","_update_horde_allowance","local HordePacing=NativeHorde; local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_MIN,TRAVEL_DISTANCE_CHANGE_ALLOWANCE_MAX=5,8")
for name in ("set_terror_event_point_modifier","get_terror_event_point_modifier","set_max_points_modifer","get_max_points_modifer"):
    L.globals()[name]=method("scripts/managers/terror_event/terror_event_manager.lua","TerrorEventManager",name,"local TerrorEventManager=NativeTerror")
L.globals().native_auto_update=method("scripts/managers/pacing/auto_event/auto_event.lua","AutoEvent","update",
    """local AutoEvent=NativeAuto
local DEFAULT_TOTAL_MINIONS_ALLOWED_HARDLIMIT,PAUSE_TRICKLE_TIME,DEFAULT_NUM_WAVES,FORCE_SKIP_CURRENT_WAVE_TIMING=145,5,3,180
local DEFAULT_PRE_STINGER_WWISE_EVENT,DEFAULT_STINGER_WWISE_EVENT="pre","start"
""")
L.execute("""
function hook(path,name)
    local target=type(path)=="string" and require(path) or path
    for _,h in ipairs(hooks) do if h.owner==B and h.target==target and h.name==name then return h.fn,h.safe end end
    error("Missing hook: "..name)
end
function configure(coarse,fine)
    B.values.native_configuration_v3=coarse or {}
    mods.HavocEnemyDirector=fine and {is_gameplay_enabled=function() return true end,get_config=function() return fine end} or nil
    Managers.state.game_session={}; E.reset(); host=true
end
local sp_path="scripts/managers/pacing/specials_pacing/specials_pacing"
local roamer_init=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","init")
local function received_seed(_,nav,template,seed,factions)return seed end
configure({},nil)
assert(roamer_init(received_seed,{},nil,{},432,{})==432,'roamer seed follows the native mission by default')
configure({},{version=2,patches={},rules={},seed=2147483646})
assert(roamer_init(received_seed,{},nil,{},432,{})==2147483646,'fixed layout seed reaches the native roamer constructor')
host=false
assert(roamer_init(received_seed,{},nil,{},432,{})==432,'clients do not override native layout randomness')
host=true
local setup=hook(sp_path,"_setup")
local entry
for _,e in ipairs(A.entries) do if e.family=="specials" and e.fields.max_alive_specials then entry=e; break end end
local base_slots=entry.root.max_alive_specials
configure({special_slots=2})
local sp={_max_alive_specials_multiplier=1.5,_max_alive_specials_bonus=2,_timer_modifier=1,
    _setup_specials_slot=function(self,slots,slot,template,timer) slot.timer=timer; slot.breed=template.breeds.all[1] end}
setup(native_special_setup,sp,entry.root)
assert(sp._max_alive_specials==math.ceil(base_slots*2*1.5+2))
assert(#sp._specials_slots==sp._max_alive_specials and entry.root.max_alive_specials==base_slots)
setup(native_special_setup,sp,sp._template)
assert(sp._max_alive_specials==math.ceil(base_slots*2*1.5+2),"Native template re-setup must not rescale")
configure({special_slots=3},{patches={[entry.id]={max_alive_specials=7}},rules={}})
setup(native_special_setup,sp,entry.root)
assert(sp._max_alive_specials==math.ceil(7*1.5+2),"Fine slots precede native multiplier and additive bonus")
-- Native templates and modifiers still supply their native faction aliases.
assert(entry.fields["breeds/all"] and entry.fields["breeds/scramblers"])
assert(S.validate_value(entry.fields["breeds/all"],{"flamer","grenadier","chaos_hound"},A.breeds))
assert(not S.validate_value(entry.fields["breeds/disablers"],{"grenadier"},A.breeds))
-- One native coordinated quota roll and one probability evaluation, no retries.
local tactic={name="test",total_num_allowed={2,2},chance=1,conditions={function() return true end},high_chance_conditions={function() return false end},high_chance=1}
local raw={coordinated_horde_strike_settings={test=tactic}}
local tactical=A.add("hordes/test_runtime","hordes",raw)
configure({coordinated_allowance=2})
local adjusted=E.prepare(raw,"hordes"); local self={_template=adjusted}
local random=math.random; local rolls=0
math.random=function(a,b) rolls=rolls+1; if a then return a end; return 0.5 end
native_horde_init(self,adjusted)
assert(self._coordinated_horde_strikes_total_num_allowed.test==4 and rolls==1)
assert(native_horde_evaluate(self,1) and rolls==2)
assert(raw.coordinated_horde_strike_settings.test.total_num_allowed[1]==2)
math.random=random
-- Replace only the explicit predicate list; retain native quota and probability.
local fine={patches={},rules={[tactical.id]={["coordinated_horde_strike_settings/test/conditions"]={mode="replace",match="all",clauses={{condition="load_max",value=20}}}}}}
configure({},fine)
Managers.state.pacing={total_challenge_rating=function() return 30 end}
adjusted=E.prepare(raw,"hordes"); self={_template=adjusted}
native_horde_init(self,adjusted)
assert(not native_horde_evaluate(self,1) and self._coordinated_horde_strikes_total_num_allowed.test==2)
Managers.state.pacing.total_challenge_rating=function() return 10 end; E.clear_context()
assert(native_horde_evaluate(self,1))
-- Native event budget composes AFTER additive word modifiers, for both budget caps.
configure({event_budget=2})
local terror={_point_modifier=1,_max_points_modifier=1}
set_terror_event_point_modifier(terror,0.5); set_terror_event_point_modifier(terror,0.25); set_max_points_modifer(terror,1.5)
local getter=hook("scripts/managers/terror_event/terror_event_manager","get_terror_event_point_modifier")
local maxgetter=hook("scripts/managers/terror_event/terror_event_manager","get_max_points_modifer")
assert(getter(get_terror_event_point_modifier,terror)==3.5 and maxgetter(get_max_points_modifer,terror)==3)
assert(terror._point_modifier==1.75 and terror._max_points_modifier==1.5)
-- Per-zone pack weights are consumed by the actual native LoadedDice algorithm.
local generate=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","_generate_roamers")
local one={name="same_name",{weight=1,breeds={"chaos_poxwalker"}},{weight=0,breeds={"renegade_melee"}}}
local two={name="same_name",{weight=0,breeds={"chaos_poxwalker"}},{weight=1,breeds={"renegade_melee"}}}
local zones={{roamer_packs=one},{roamer_packs=two}}
local roamer={_roamer_pack_probabilities={}}
local Dice=require("scripts/utilities/loaded_dice")
generate(function(self,z)
    assert(z[1].roamer_packs.name~=z[2].roamer_packs.name)
    for i=1,2 do
        local p=self._roamer_pack_probabilities[z[i].roamer_packs.name]
        for n=1,100 do assert(Dice.roll(p.prob,p.alias)==i) end
    end
end,roamer,zones,{})
assert(one.name=="same_name" and two.name=="same_name")
-- Root eligibility denies fresh encounters but ongoing native waves continue.
local eligibility={mode="append",match="all",clauses={{condition="load_max",value=20}}}
local hentry=A.add("hordes/test_gate","hordes",{max_active_minions=100})
configure({}, {patches={},rules={[hentry.id]={encounter=eligibility}}})
Managers.state.pacing={total_challenge_rating=function() return 30 end,get_mission_progression=function() return 100,0 end}
local hp={_template=E.prepare(hentry.root,"hordes"),_required_travel_distance=10,_triggered_hordes=0,_old_furthest_travel_distance=0,_current_wave=0}
local pm={_horde_pacing=hp,_target_side_id=1}
local allow=hook("scripts/managers/pacing/pacing_manager","spawn_type_enabled")
Managers.state.pacing.spawn_type_enabled=function() return allow(function() return true end,pm,"hordes") end
Managers.state.minion_spawn={num_spawned_minions=function() return 0 end}
assert(not native_horde_allowance(hp,10,0.1,2,1))
hp._current_wave=1
assert(native_horde_allowance(hp,10,0.1,2,1),"An ongoing horde still uses native completion")
-- An automatic event holds its first wave, then runs and cleans up natively.
local auto_entry=A.add("events/test_auto","events",{waves_cooldown={{1,1}},cooldown={{1,1}},num_waves_by_resistance={2}})
configure({}, {patches={},rules={[auto_entry.id]={encounter=eligibility}}})
Managers.state.difficulty={get_table_entry_by_resistance=function(_,t) return t[1] end}
Managers.state.extension={system=function() return {get_side=function() return {} end} end}
Managers.state.minion_spawn={total_allocated_num_enemies=function() return 0 end}
Managers.event={trigger=function() end}
-- Supply a known context; state collection itself is covered separately.
E.context=function() return {load=30} end
local data={pre_stinger_delay=0,wave_cooldown=0,waves_to_spawn=2,position={unbox=function() return {} end},groups={}}
local auto={_template=E.prepare(auto_entry.root,"events"),_active_events={test=data},_target_side_id=1,_side_id=2,
    _check_num_events=function() end,_fx_system={trigger_wwise_event=function() end},_try_inject_special=function() end,
    execute=function(self) self.executions=(self.executions or 0)+1 end}
local update=hook("scripts/managers/pacing/auto_event/auto_event","update")
update(native_auto_update,auto,0.1,10)
assert(data.waves_to_spawn==2 and not data.primary_wave_event_sent and not auto.executions and data.wave_cooldown>10)
E.context=function() return {load=10} end
update(native_auto_update,auto,0.1,11)
assert(data.waves_to_spawn==1 and data.primary_wave_event_sent and auto.executions==1)
E.context=function() return {load=30} end
update(native_auto_update,auto,0.1,13)
assert(data.waves_to_spawn==0 and auto.executions==2,"An already-started encounter completes its waves")
-- Mission battle nodes wait without consuming quota or changing native nodes.
local raw_event={{"spawn_by_points",points=30},{"continue_when",condition=function() return true end}}
local event_entry=A.add("mission_events/test/start","mission_events",raw_event)
configure({}, {patches={},rules={[event_entry.id]={["1/start"]=eligibility}}})
local event=E.prepare(raw_event,"mission_events"); local scratch={}
local node_update=hook(require("scripts/managers/terror_event/terror_event_nodes").spawn_by_points,"update")
local calls=0; local function proceed() calls=calls+1; return true end
assert(not node_update(proceed,event[1],scratch,1,0.1) and calls==0 and not scratch.started_spawn)
scratch.started_spawn=true
assert(node_update(proceed,event[1],scratch,1,0.1) and calls==1)
assert(raw_event[1].points==30 and event[2]==raw_event[2])
host=false
assert(node_update(proceed,event[1],{},1,0.1) and calls==2)
""")
print("Actual native special slots, coordinated quota/RNG, event budget, weighted packs, horde continuation and automatic-event waiting/completion: PASS")
