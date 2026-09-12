"""Exercise capacity and wave pacing against the game's own consumers."""
from native_harness import *


def extract(path, owner, name):
    source = (GAME/path).read_text(encoding='utf-8-sig')
    start = source.index(owner+'.'+name+' = function')
    return source[start:source.index('\nend', start)+4]


L.execute('NativePacing={};ReferencePacing={};NativeHorde={};function table.clear(t) for k in pairs(t) do t[k]=nil end end')
pacing_source = extract('scripts/managers/pacing/pacing_manager.lua', 'PacingManager', 'spawn_type_enabled')
L.execute('local PacingManager=NativePacing;local HARD_ALLOCATED_LIMIT=145;'+pacing_source)
# A reference with the literal threshold replaced; all decision order and
# conditions are the unmodified native function, independent of the hook.
L.execute('local PacingManager=ReferencePacing;'+pacing_source.replace('HARD_ALLOCATED_LIMIT', 'reference_capacity'))
for name in ('_update_horde_allowance', '_update_horde_pacing'):
    L.execute('''local HordePacing=NativeHorde
local TRAVEL_DISTANCE_CHANGE_ALLOWANCE_MIN,TRAVEL_DISTANCE_CHANGE_ALLOWANCE_MAX=5,8
local HORDE_FAILED_WAIT_TIME=3
local CHALLENGE_RATING_FOR_NO_MOVE_TIMER_OVERRIDE=0
local TIME_SINCE_FORWARD_TRAVEL_CHANGE_MOVE_TIMER_OVERRIDE={60,60,60,15,10}
'''+extract('scripts/managers/pacing/horde_pacing/horde_pacing.lua', 'HordePacing', name))
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks')
L.globals().Profile = load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile')
L.execute('''
local target=require("scripts/managers/pacing/pacing_manager")
local admission
for _,h in ipairs(hooks) do if h.target==target and h.name=="spawn_type_enabled" then admission=h.fn end end
assert(admission)
local allocated=0
Managers.state.minion_spawn={total_allocated_num_enemies=function() return allocated end,num_spawned_minions=function() return allocated end}
local function configure(coarse)
 B.values.native_configuration_v3=coarse or {};Managers.state.game_session={};E.reset();host=true
end
capacity_cases=0
for _,factor in ipairs({.5,1,1.75,3,10}) do
 configure({combat_tolerance=factor})
 reference_capacity=math.floor(145*factor+.5)
 for _,count in ipairs({0,72,73,94,95,144,145,146,253,254,284,285,434,435,436,1450,1451}) do
  allocated=count
  for mask=0,63 do
   local disabled=mask%2==1
   local paused=math.floor(mask/2)%2==1
   local state_allowed=math.floor(mask/4)%2==1
   local heat_active=math.floor(mask/8)%2==1
   local heat_allowed=math.floor(mask/16)%2==1
   local challenge=math.floor(mask/32)%2==1 and 201 or 0
   for _,source in ipairs({"hordes","specials","roamers","terror_events","monsters"}) do
    local p={_disabled=disabled,_challenge_rating_thresholds={[source]=200},_total_challenge_rating=challenge,
     _paused_spawn_types={[source]=paused},_allowed_spawn_types={[source]=state_allowed},
     _heat_pacing={active=function() return heat_active end,current_stage_settings=function() return {allowed_spawn_types={[source]=heat_allowed}} end}}
    local expected,expected_reason=ReferencePacing.spawn_type_enabled(p,source)
    local actual,reason=admission(NativePacing.spawn_type_enabled,p,source)
    assert(actual==expected,"capacity decision differs from native reference")
    -- Below baseline, an earlier native refusal retains its own reason.
    if factor>=1 then assert(reason==expected_reason,"lost native refusal: "..tostring(expected_reason)) end
    capacity_cases=capacity_cases+1
   end
  end
 end
end
configure({combat_tolerance=3});allocated=200
local p={_challenge_rating_thresholds={},_total_challenge_rating=0,_paused_spawn_types={},_allowed_spawn_types={hordes=true},_heat_pacing={active=function() return false end}}
assert(admission(NativePacing.spawn_type_enabled,p,"hordes"))
host=false;assert(not admission(NativePacing.spawn_type_enabled,p,"hordes"));host=true
configure({});assert(not admission(NativePacing.spawn_type_enabled,p,"hordes"))
configure({combat_tolerance=3})
local fine_allowed=E.allowed
E.allowed=function() return false end
p._horde_pacing={_template={}}
local allowed,reason=admission(NativePacing.spawn_type_enabled,p,"hordes")
assert(not allowed and reason=="HCM_condition","expanded capacity must not bypass HED predicates")
E.allowed=fine_allowed

local base=require("scripts/managers/pacing/pacing_templates").default.horde_pacing_template.resistance_templates[5]
local updated=S.apply(base,"hordes",Profile.values(10),nil,A.breeds,A.by_table)
assert(base.max_active_minions==95 and updated.max_active_minions==190)
assert(base.max_active_minions_for_ambush==50 and updated.max_active_minions_for_ambush==100)
assert(updated.num_waves.far_vector_horde==3 and updated.num_waves.ambush_horde==1)
assert(math.abs(updated.time_between_waves-10/1.2)<.000001)
Managers.state.pacing={get_mission_progression=function() return 10000,0 end,spawn_type_enabled=function() return true end,
 get_ramp_up_frequency_modifier=function() return 1 end,num_aggroed_monsters=function() return 0 end,total_challenge_rating=function() return 0 end}
local h={_template=base,_required_travel_distance=10,_triggered_hordes=0,_current_wave=1,_old_furthest_travel_distance=10000}
allocated=100;assert(not NativeHorde._update_horde_allowance(h,1,.016,2,1))
h._template=updated;assert(NativeHorde._update_horde_allowance(h,1,.016,2,1))
allocated=190;assert(not NativeHorde._update_horde_allowance(h,1,.016,2,1))
allocated=189;assert(NativeHorde._update_horde_allowance(h,1,.016,2,1))

Managers.state.difficulty={get_table_entry_by_resistance=function(_,t) return t[5] end}
Managers.state.mutator={mutator=function() return false end}
Managers.event={trigger=function() end}
local function run_episode(template,count)
 allocated=count
 local waves=0
 local self={_template=template,_required_travel_distance=10,_triggered_hordes=0,_current_wave=0,_old_furthest_travel_distance=10000,
  _horde_timer=0,_next_horde_at=0,_rate_modifier=1,_current_horde_type="far_vector_horde",
  _spawn_horde_wave=function() waves=waves+1;return true end,_first_horde_wave_spawn=function() end,
  _setup_next_horde=function(s) s._next_horde_at=math.huge end}
 for frame=0,2700 do
  local t=frame/60
  if NativeHorde._update_horde_allowance(self,t,1/60,2,1) then NativeHorde._update_horde_pacing(self,t,1/60,2,1) end
 end
 return waves
end
local old=S.copy(updated);old.max_active_minions=285;old.max_active_minions_for_ambush=150;old.time_between_waves=10/2.25;old.num_waves.far_vector_horde=18
episode_baseline=run_episode(base,0);episode_old=run_episode(old,0);episode_updated=run_episode(updated,0)
assert(episode_baseline==3 and episode_old==11 and episode_updated==3)
assert(run_episode(old,100)==11 and run_episode(updated,100)==3)
assert(run_episode(updated,190)==0)
-- Explicit HED values retain precedence over broad capacity/frequency settings.
local precise=S.apply(base,"hordes",Profile.values(10),{max_active_minions=111,time_between_waves=7},A.breeds,A.by_table)
assert(precise.max_active_minions==111 and precise.time_between_waves==7)
local specials=require("scripts/managers/pacing/pacing_templates").default.specials_pacing_template.resistance_templates[5]
local sp=S.apply(specials,"specials",Profile.values(10),nil,A.breeds,A.by_table)
assert(sp.max_alive_specials==24 and sp.max_of_same.chaos_hound==6 and sp.max_of_same.cultist_mutant==12)
local function check_quotas(base,compiled)
 for key,value in pairs(base) do
  if type(value)=="table" then check_quotas(value,compiled[key]) else assert(compiled[key]==value*3) end
 end
end
check_quotas(specials.num_allowed_disablers_per_alive_targets,sp.num_allowed_disablers_per_alive_targets)
assert(S.equal(sp.breeds,specials.breeds) and specials.max_of_same.chaos_hound==2)
''')
print('Native capacity decisions, challenge/mission/heat pauses, default and remote behavior, and HED gates:', L.globals().capacity_cases, 'PASS')
print('Difficulty-5 follow-up threshold 95 -> 190; 100-enemy baseline stall corrected; reduced 190 cap still pauses: PASS')
print('One 45-second native horde episode at low load: baseline/3.3.0/updated waves =', L.globals().episode_baseline, L.globals().episode_old, L.globals().episode_updated, '(not a gameplay spawn-rate measurement): PASS')
print('Same-breed and finite player-dependent disabler quotas scale; native breed choices and precise HED overrides preserved: PASS')
