"""Check the actual specialist slot, burst and disabler consumers."""
from native_harness import *


source=(GAME/'scripts/managers/pacing/specials_pacing/specials_pacing.lua').read_text(encoding='utf-8-sig')
def extract(name):
    start=source.index('SpecialsPacing.'+name+' = function')
    return source[start:source.index('\nend',start)+4]


L.execute('''NativeSpecial={};function table.clear(t) for k in pairs(t) do t[k]=nil end end;function table.shuffle(t) return t end''')
prefix='''local SpecialsPacing=NativeSpecial
local Breeds=require("scripts/settings/breed/breeds")
local USED_BREEDS={};local DEFAULT_MIN_TIMER_DIFF_RANGE={3,5}
local MIN_COORDINATED_TIMER=20;local COORDINATED_STRIKE_TIMER_OFFSET_RANGE={3,6}
local PlayerUnitStatus={requires_help=function() return false end}
'''
names=('_setup_specials_slot','_setup','_get_breed_name','_get_special_slot_breed_name','_check_monster_override','_check_disabler_override','_check_and_activate_coordinated_strike')
L.execute(prefix+'\n'.join(extract(n) for n in names))
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks')
L.globals().Profile=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile')
L.execute('''
local class=require("scripts/managers/pacing/specials_pacing/specials_pacing")
local slot_hook,strike_hook
for _,h in ipairs(hooks) do
 if h.target==class and h.name=="_setup_specials_slot" then slot_hook=h.fn end
 if h.target==class and h.name=="_check_and_activate_coordinated_strike" then strike_hook=h.fn end
end
assert(slot_hook and strike_hook)
local random=math.random
math.random=function(a,b) if b then return a end;if a then return 1 end;return .5 end
local clock=0
Managers.time={time=function() return clock end}
Managers.state.pacing={current_faction=function() return "renegade" end,num_aggroed_monsters=function() return 0 end}
Managers.state.terror_event={num_active_events=function() return 0 end}
Managers.state.difficulty={get_table_entry_by_challenge=function(_,t) return t[5] end}
Managers.state.extension={system=function() return {get_side=function() return {valid_player_units={"player"}} end} end}
ScriptUnit={extension=function() return {read_component=function() return {} end} end}
local base=require("scripts/managers/pacing/pacing_templates").default.specials_pacing_template.resistance_templates[5]
local updated=S.apply(base,"specials",Profile.values(10),nil,A.breeds,A.by_table)
local old=S.copy(updated)
old.max_of_same=S.copy(base.max_of_same)
old.num_allowed_disablers_per_alive_targets=S.copy(base.num_allowed_disablers_per_alive_targets)
old.coordinated_strike_num_breeds=S.copy(base.coordinated_strike_num_breeds)
old.coordinated_strike_timer_range=S.copy(base.coordinated_strike_timer_range)
old.coordinated_surge_timer_range=S.copy(base.coordinated_surge_timer_range)
old.min_timer_diff_range=base.min_timer_diff_range
local function configure(frequency)
 B.values.native_configuration_v3={special_frequency=frequency};Managers.state.game_session={};E.reset();host=true
end
local function create(template,hooked)
 local self=setmetatable({_max_alive_specials_multiplier=1,_max_alive_specials_bonus=0,_timer_modifier=1}, {__index=NativeSpecial})
 if hooked then
  self._setup_specials_slot=function(s,...) return slot_hook(NativeSpecial._setup_specials_slot,s,...) end
  self._check_and_activate_coordinated_strike=function(s,...) return strike_hook(NativeSpecial._check_and_activate_coordinated_strike,s,...) end
 end
 self:_setup(template,template.first_spawn_timer_modifer)
 return self
end
configure(3.25)
local default_manager,old_manager,new_manager=create(base,false),create(old,false),create(updated,true)
assert(#default_manager._specials_slots==8 and #old_manager._specials_slots==24 and #new_manager._specials_slots==24)
initial_timers={}
for _,manager in ipairs({default_manager,old_manager,new_manager}) do
 local first,last=math.huge,0
 for _,slot in ipairs(manager._specials_slots) do first=math.min(first,slot.spawn_timer);last=math.max(last,slot.spawn_timer) end
 initial_timers[#initial_timers+1]={first=first,last=last}
end
assert(math.abs(initial_timers[1].last-124)<.001)
assert(initial_timers[2].last>120 and initial_timers[3].last<59)
assert(math.abs(updated.min_timer_diff_range[1]-3/3.25)<.000001)
assert(base.min_timer_diff_range==nil,"never write fallback values into native templates")
-- Ordinary windows, coordinated windows and surge windows all use frequency.
for _,key in ipairs({"timer_range","coordinated_strike_timer_range","coordinated_surge_timer_range"}) do
 for i=1,2 do assert(math.abs(updated[key][i]-base[key][i]/3.25)<.000001) end
end
-- The target-count rule remains active with its scaled finite allowance.
local function disabler_case(template,active)
 local manager=create(template,true)
 for _,slot in ipairs(manager._specials_slots) do slot.disabler_is_active=nil end
 for i=1,active do manager._specials_slots[i].disabler_is_active=true end
 local slot={breed_name="chaos_hound"}
 return manager:_check_disabler_override(template,1,slot),slot
end
local replaced,slot=disabler_case(old,1);assert(replaced and slot.disabler_override)
replaced,slot=disabler_case(updated,2);assert(not replaced and slot.breed_name=="chaos_hound")
replaced,slot=disabler_case(updated,3);assert(replaced and slot.disabler_override)
assert(updated.num_allowed_disablers_per_alive_targets[5][1]==3 and old.num_allowed_disablers_per_alive_targets[5][1]==1)
-- Test an eligible coordinated attack, leaving native chance/eligibility code.
local function strike(template,hooked)
 template=S.copy(template);template.chance_for_coordinated_strike=1;template.coordinated_surge_chance=0
 local manager=create(template,hooked)
 assert(manager:_check_and_activate_coordinated_strike(template,manager._specials_slots[1]))
 local timers={}
 for _,slot in ipairs(manager._specials_slots) do if slot.coordinated_strike then timers[#timers+1]=slot.spawn_timer end end
 table.sort(timers)
 return timers,manager
end
local old_strike=strike(old,false)
local new_strike,manager=strike(updated,true)
assert(#old_strike==6 and #new_strike==18)
assert(math.abs(old_strike[2]-old_strike[1]-4.5)<.000001)
assert(math.abs(new_strike[2]-new_strike[1]-4.5/3.25)<.000001)
coordinated_old={count=#old_strike,first=old_strike[1],last=old_strike[#old_strike]}
coordinated_new={count=#new_strike,first=new_strike[1],last=new_strike[#new_strike]}
-- Ongoing surge timers are already scaled; do not scale them twice.
manager._coordinated_surge_duration=100
assert(manager:_check_and_activate_coordinated_strike(updated,manager._specials_slots[1]))
surge_timer=manager._specials_slots[1].spawn_timer
assert(math.abs(surge_timer-12/3.25)<.000001)
-- Explicit non-strike injection timers must pass through without adjustment.
local injected={}
slot_hook(NativeSpecial._setup_specials_slot,manager,manager._specials_slots,injected,updated,1,"chaos_hound",20,true)
assert(injected.spawn_timer==20 and injected.injected)
local ok=pcall(strike_hook,function() error("expected strike failure") end,manager,updated,injected)
assert(not ok)
slot_hook(NativeSpecial._setup_specials_slot,manager,manager._specials_slots,injected,updated,1,"chaos_hound",20,true)
assert(injected.spawn_timer==20)
-- Disabling local authority preserves the native offsets, even on a prepared template.
host=false
local remote=strike(updated,true)
assert(math.abs(remote[2]-remote[1]-4.5)<.000001);host=true
configure(1)
local unchanged=strike(base,true)
assert(#unchanged==6 and math.abs(unchanged[2]-unchanged[1]-4.5)<.000001)
math.random=random
''')
def convert(t): return [{k:v for k,v in row.items()} for _,row in t.items()]
print('Native initial slot timers, baseline/3.2.1/updated:', convert(L.globals().initial_timers), 'PASS')
print('Native single-player disabler allowance 1 -> 3, with substitution beyond the allowance and unchanged breed choices: PASS')
print('Native eligible coordinated attack, old/new:', dict(L.globals().coordinated_old.items()), dict(L.globals().coordinated_new.items()), 'PASS')
print('Native ongoing surge timer 12 ->', L.globals().surge_timer, '; no double scaling, injection changes, remote changes or leaked strike context: PASS')
