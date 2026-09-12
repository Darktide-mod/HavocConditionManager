"""Verify every intensity against actual native templates, not just anchors."""
from native_harness import *
import json
L.globals().Profile=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile")
L.globals().Elite=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/elite_composition")
L.execute('''
assert(not Profile.values(0) and not Profile.values(11) and not Profile.values(5.5))
assert(S.equal(Profile.values(1),S.coarse_config()))
local previous
for level=1,10 do
 local cfg=Profile.values(level)
 assert(Profile.match(cfg)==level)
 for _,d in ipairs(S.coarse) do
  assert(cfg[d.id]>=d.min and cfg[d.id]<=d.max)
  if previous then
   if d.id=="recovery_duration" then assert(cfg[d.id]<=previous[d.id]) else assert(cfg[d.id]>=previous[d.id]) end
  end
  if not Profile.anchors[d.id] then assert(cfg[d.id]==1) end
 end
 previous=cfg
end
local five,ten=Profile.values(5),Profile.values(10)
assert(five.patrols==3 and five.monster_encounters==4 and five.special_slots==2 and five.special_frequency==2)
assert(five.horde_waves==1 and five.horde_size==1.1 and five.horde_frequency==1.08 and five.ramp_strength==1)
assert(ten.patrols==6 and ten.monster_encounters==8 and ten.special_slots==3 and ten.horde_waves==1)
assert(five.special_slots*five.special_frequency==4 and ten.special_slots*ten.special_frequency==9.75)
local changed=S.copy(five);changed.horde_size=1.25;assert(not Profile.match(changed))
local old={};for _,d in ipairs(S.coarse) do old[d.id]=5 end;assert(not Profile.match(old))
local isolated=Profile.values(5);isolated.horde_size=10;assert(Profile.values(5).horde_size==1.1)
local unchanged={num_to_spawn=true,num_to_spawn_per_mission=true,ramp_modifiers=true,max_active_hordes=true,max_spawned_per_section=true,position_offset=true,num_waves=true}
local decreasing={horde_timer_range=true,travel_distance_required_for_horde=true,time_between_waves=true,
 trickle_horde_travel_distance_range=true,trickle_horde_cooldown=true,timer_range=true,min_timer_diff_range=true,
 coordinated_strike_timer_range=true,coordinated_surge_timer_range=true,monster_timer_range=true,duration=true}
profile_checked=0;category_checked=0;compiled_levels={}
for level=1,10 do
 local cfg=Profile.values(level)
 local totals={common=0,elite=0,other=0}
 B.values.native_configuration_v3=cfg;Managers.state.game_session={};E.reset()
 for _,entry in ipairs(A.entries) do
  local compiled=E.prepare(entry.root,entry.family)
  if level==1 then assert(compiled==entry.root,"level 1 copied native template: "..entry.id) end
  local previous=level>1 and S.apply(entry.root,entry.family,Profile.values(level-1),nil,A.breeds,A.by_table)
  for _,item in ipairs(entry.items) do
   local value=S.get(compiled,item.path)
   local before=previous and S.get(previous,item.path)
   if item.kind=="composition" then
    for i,v in ipairs(value) do
     assert(v.name==item.value[i].name)
     local role=Elite.role(A.breeds,v.name) or "other"
     totals[role]=totals[role]+v.amount[2]
     for j=1,2 do
      assert(v.amount[j]>=item.value[i].amount[j],"below native category count: "..entry.id.."/"..item.id)
      if before then assert(v.amount[j]>=before[i].amount[j],"category count declined: "..entry.id.."/"..item.id) end
      if role=="other" then assert(v.amount[j]==item.value[i].amount[j]) end
      category_checked=category_checked+1
     end
    end
   elseif item.kind=="pool" then
    local counts,old={},{}
    for _,name in ipairs(value) do counts[name]=(counts[name] or 0)+1 end
    for _,name in ipairs(before or item.value) do old[name]=(old[name] or 0)+1 end
    for name,n in pairs(old) do assert((counts[name] or 0)>=n,"pool lost breed members: "..entry.id.."/"..item.id) end
   elseif item.kind=="number" or item.kind=="range" then
    local a=type(value)=="table" and value or {value}
    local b=type(before)=="table" and before or {before}
    if before then for i,n in ipairs(a) do
     if decreasing[item.definition.key] then assert(n<=b[i],"interval grew: "..entry.id.."/"..item.id)
     else assert(n>=b[i],"native allowance declined: "..entry.id.."/"..item.id) end
    end end
   end
   if unchanged[item.definition.key] or item.definition.key=="time_between_waves" and (entry.family~="hordes" or item.id:find("trickle",1,true) or item.id:find("coordinated_horde_strike_settings",1,true)) then
    assert(S.equal(value,item.value),entry.id.."/"..item.id);profile_checked=profile_checked+1
   end
  end
 end
 compiled_levels[level]=totals
end
''')
# The immutable old release supplies the migration fixture independently.
import zipfile
with zipfile.ZipFile(PROJECT/'release/3.4.0/HavocConditionManager-3.4.0.zip') as archive:
    legacy=L.execute(archive.read('HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile.lua').decode('utf-8-sig'))
for level in range(1,11):
    raw=legacy['values'](level);raw['coordinated_load']=None
    L.globals().legacy_raw=raw
    L.execute(f'local migrated,level=Profile.migrate(legacy_raw);assert(level=={level} and S.equal(migrated,Profile.values({level})))')
    raw['horde_size']=4.33
    assert L.globals().Profile['migrate'](raw) is None
assert L.globals().Profile['migrate'](L.table_from({})) is None
report={str(level):{d.id:L.globals().Profile['values'](level)[d.id] for _,d in L.globals().S.coarse.items()} for level in range(1,11)}
(CHECKS/'intensity-profiles.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('All ten levels: native baseline identity, monotone per-breed composition/patrol counts and allowances, inverse intervals, exact old-preset migration and custom preservation: PASS')
print('Native template checks:',L.globals().profile_checked,'preserved fields;',L.globals().category_checked,'category amount checks: PASS')
