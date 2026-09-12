"""Verify independent category growth and native point-pool/roamer consumers."""
from native_harness import *

def extract(path, owner, name):
    source = (GAME/path).read_text(encoding='utf-8-sig')
    start = source.index(owner+'.'+name+' = function')
    return source[start:source.index('\nend', start)+4]

L.globals().Elite=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/elite_composition')
L.globals().Profile=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile')
L.execute('''
composition_cases=0;changed_pools=0
for _,entry in ipairs(A.entries) do
 for _,item in ipairs(entry.items) do
  if item.kind=="composition" then
   local baseline=S.copy(item.value)
   for _,size in ipairs({.25,.65,1,1.35,3}) do
    local sized=S.scaled(item,entry.family,S.coarse_config({horde_size=size,trickle_size=size}),A.breeds)
    for _,bias in ipairs({.25,1,1.75,3,10}) do
     local result=S.scaled(item,entry.family,S.coarse_config({horde_size=size,trickle_size=size,elite_density=bias}),A.breeds)
     assert(#result==#sized)
     for i,v in ipairs(result) do
      local kind=Elite.role(A.breeds,v.name)
      local common=(entry.family=="hordes" or entry.family=="mutators") and size or 1
      local factor=kind=="elite" and bias or kind=="common" and common or 1
      assert(v.name==item.value[i].name and v.amount[1]>=0 and v.amount[2]>=v.amount[1])
      for j=1,2 do assert(v.amount[j]==math.floor(item.value[i].amount[j]*factor+.5),entry.id.."/"..item.id) end
      if not kind then assert(S.equal(v,item.value[i])) end
     end
     composition_cases=composition_cases+1
    end
   end
   assert(S.equal(baseline,item.value))
  elseif item.kind=="pool" then
   local result=S.scaled(item,entry.family,S.coarse_config({elite_density=3}),A.breeds)
   local before,after={},{}
   for _,name in ipairs(item.value) do before[name]=(before[name] or 0)+1 end
   for _,name in ipairs(result) do assert(before[name]);after[name]=(after[name] or 0)+1 end
   for name,count in pairs(before) do
    local scaled=entry.family=="monsters" and item.id:find("breed_lists/",1,true) and Elite.role(A.breeds,name)=="elite"
    assert(after[name]==count*(scaled and 3 or 1),entry.id.."/"..item.id.."/"..name)
   end
   if not S.equal(result,item.value) then
    changed_pools=changed_pools+1
    assert(Elite.fraction(result,A.breeds)>=Elite.fraction(item.value,A.breeds))
    if changed_pools<=3 then
    local precise=S.apply(entry.root,entry.family,S.coarse_config({elite_density=3}),{[item.id]=item.value},A.breeds,A.by_table)
    assert(S.equal(S.get(precise,item.path),item.value),"HED pool override lost")
    end
   end
  end
 end
end
assert(composition_cases>1000 and changed_pools>0)
local patrol={}
for i=1,8 do patrol[#patrol+1]="renegade_executor";patrol[#patrol+1]="renegade_melee" end
assert(Elite.fraction(patrol,A.breeds)==.5)
assert(Elite.fraction(Elite.list(patrol,3,A.breeds),A.breeds)==.75)
assert(#Elite.list(patrol,3,A.breeds)==32)
''')

# Native breed costs and exact native selection functions; no synthetic scoring.
costs=lua_file(GAME/'scripts/settings/breed/breed_terror_event_settings.lua')
for name,breed in cache['scripts/settings/breed/breeds'].items():
    if costs[name]: breed.point_cost=costs[name].point_cost
L.globals().NativeBreeds=cache['scripts/settings/breed/breeds']
L.globals().LoadedDice=lua_file(GAME/'scripts/utilities/loaded_dice.lua')
L.execute('''
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.clear_array(t) for i=#t,1,-1 do t[i]=nil end end
function table.shuffle(t) for i=#t,2,-1 do local j=math.random(i);t[i],t[j]=t[j],t[i] end end
BreedQueries={};NativeEvent={}
''')
L.execute('local minion_breeds_array={};for name,breed in pairs(NativeBreeds) do if breed.breed_type=="minion" then minion_breeds_array[#minion_breeds_array+1]=breed end end;table.sort(minion_breeds_array,function(a,b) return a.name<b.name end);'+extract('scripts/utilities/breed_queries.lua','BreedQueries','match_minions_by_tags'))
L.execute('local affordable_breeds={};'+extract('scripts/utilities/breed_queries.lua','BreedQueries','pick_random_minion_by_points'))
L.execute('local AutoEvent=NativeEvent;local breeds_to_spawn={};local SPAWN_SIDE_NAME="villains";local DEFAULT_TOTAL_MINIONS_ALLOWED_BEFORE_CUTOFF=115;'+extract('scripts/managers/pacing/auto_event/auto_event.lua','AutoEvent','_compose_spawn_list'))
L.execute('''
Managers.state.minion_spawn={num_spawned_minions=function() return 0 end}
Managers.state.difficulty={get_table_entry_by_resistance=function(_,t) return t[5] end}
Managers.state.pacing={current_faction=function() return "renegade" end}
Managers.state.game_mode={settings=function() return {side_sub_faction_types={villains={"renegade","cultist"}}} end}
local template=require("scripts/managers/pacing/auto_event/templates/auto_event_templates").dummy_auto_event_template
assert(template)
local updated=S.copy((S.apply(template,"events",Profile.values(10),nil,A.breeds,A.by_table)))
local previous=S.copy((S.apply(template,"events",Profile.values(1),nil,A.breeds,A.by_table)))
assert(not S.equal(template.points_base,updated.points_base))
assert(S.equal(template.composition,updated.composition),"point-budget selection ratios changed")
for _,key in ipairs({"captains_settings","monster_settings","twins_settings"}) do assert(S.equal(template[key],updated[key])) end
local function simulate(t)
 math.randomseed(903410)
 local counts={elite=0,common=0,other=0,events=0}
 local keys={};for key in pairs(t.composition) do keys[#keys+1]=key end;table.sort(keys)
 for _,kind in ipairs(keys) do
  for trial=1,1000 do
   local result,count=NativeEvent._compose_spawn_list({_template=t,_num_active_events=0},{composition_type=kind,size_multiplier=1})
   for _,name in ipairs(result) do local role=Elite.role(A.breeds,name) or "other";counts[role]=counts[role]+1 end
   counts.events=counts.events+1
  end
 end
 return counts
end
event_old=simulate(previous);event_new=simulate(updated)
assert(event_new.common>event_old.common,"native events did not gain ordinary enemies")
assert(event_new.elite>event_old.elite,"native events did not gain elites")

''')

# Exercise the real per-zone consumer with both native limit representations.
L.execute('NativeRoamer={};ZONE_BREED_COUNT={};ZONE_BREED_TAG_COUNT={};ZONE_BREED_LIMITATIONS_COUNT={}')
L.execute('local RoamerPacing=NativeRoamer;local Breeds=NativeBreeds;'+extract('scripts/managers/pacing/roamer_pacing/roamer_pacing.lua','RoamerPacing','_limit_roamer_breeds'))
L.execute('''
local numeric,table_limit
for _,entry in ipairs(A.entries) do
 if entry.family=="roamers" then
  local compiled=S.apply(entry.root,entry.family,S.coarse_config({roamer_population=3}),nil,A.breeds,A.by_table)
  for _,item in ipairs(entry.items) do
   if Elite.role(A.breeds,item.breed_name)=="elite" and (item.definition.key=="breed_limit" or item.definition.key=="max") and type(item.value)=="number" and item.value>0 then
    local path=S.copy(item.path);path[#path]=nil
    if item.definition.key=="max" then path[#path]=nil end
    local before,after=S.get(entry.root,path),S.get(compiled,path)
    local breed=item.breed_name
    if before.replacements and before.replacements[breed] then
     local faction=next(before.replacements[breed])
     local function consume(settings)
      ZONE_BREED_COUNT={};ZONE_BREED_TAG_COUNT={};ZONE_BREED_LIMITATIONS_COUNT={}
      local self={_random=function(_,a,b) return a end}
      local count=0
      for i=1,item.value+1 do
       local replacement,skip=NativeRoamer._limit_roamer_breeds(self,breed,settings,faction)
       if not replacement and not skip then count=count+1 end
      end
      return count
     end
     assert(consume(before)==item.value)
     assert(consume(after)==item.value+1)
     if item.definition.key=="max" then
      table_limit=true
      if not numeric then
       local source={limits=S.copy(before)};source.limits[breed]=item.value
       local compiled=S.apply(source,"roamers",S.coarse_config({roamer_population=3}),nil,A.breeds)
       assert(compiled.limits[breed]==item.value*3)
       assert(consume(source.limits)==item.value and consume(compiled.limits)==item.value+1)
       numeric=true
      end
     else numeric=true end
    end
   end
  end
 end
end
assert(numeric and table_limit,"both native limit types must be covered: "..tostring(numeric).."/"..tostring(table_limit))
''')
report={"composition_cases":L.globals().composition_cases,"changed_pools":L.globals().changed_pools,
        "native_event_previous":dict(L.globals().event_old.items()),"native_event_updated":dict(L.globals().event_new.items())}
(CHECKS/'elite-balance.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Independent native category amounts, breed eligibility, immutable inputs and HED overrides:',report,'PASS')
print('Native event selection uses actual point costs; native numeric and table roamer limits admit the intended extra elites: PASS')
