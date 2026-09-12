"""Run actual slot placement with a lifetime-checking engine scratch allocator."""
from native_harness import *
L.execute("""
math.two_pi=math.pi*2
scratch={used=0,peak=0,objects={},restores=0}
local function check(v) assert(v.live,"temporary vector used after rewind") end
function vec(x,y,z)
 scratch.used=scratch.used+16;scratch.peak=math.max(scratch.peak,scratch.used)
 local v={x,y,z,live=true};scratch.objects[#scratch.objects+1]={offset=scratch.used,value=v};return v
end
function Script.temp_byte_count() return scratch.used end
function Script.set_temp_byte_count(n)
 assert(n<=scratch.used);scratch.restores=scratch.restores+1
 for i=#scratch.objects,1,-1 do local o=scratch.objects[i];if o.offset<=n then break end;o.value.live=false;scratch.objects[i]=nil end
 scratch.used=n
end
Vector3=function(x,y,z) return vec(x,y,z) end
Quaternion={look=function(v) check(v);return vec(v[1],v[2],v[3]) end}
function Vector3Box(v)
 check(v);local x,y,z=v[1],v[2],v[3]
 return {unbox=function() return vec(x,y,z) end,coords={x,y,z}}
end
QuaternionBox=Vector3Box
GwNavQueries={flood_fill_from_position=function(_,position,above,below,n,out)
 check(position);for i=1,n do out[i]=vec(position[1]+i,position[2],position[3]) end;return n
end}
NativeRoamer={}
""")
cache['scripts/utilities/nav_queries']=tbl({})
placements=lua_file(game/'scripts/settings/roamer/roamer_slot_placement_functions.lua')
L.globals().placements=placements
source=(game/'scripts/managers/pacing/roamer_pacing/roamer_pacing.lua').read_text(encoding='utf-8')
for name in ('_create_sub_zone_location','_create_sub_zones'):
    start=source.index('RoamerPacing.'+name+' = function');end=source.index('\nend',start)+4
    L.execute('local RoamerPacing=NativeRoamer; local RoamerSlotPlacementFunctions=placements;'+source[start:end])
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks')
L.globals().roamer_class=cache['scripts/managers/pacing/roamer_pacing/roamer_pacing']
L.execute("""
local guarded
for _,h in ipairs(hooks) do if h.target==roamer_class and h.name=="_create_sub_zone_location" then guarded=h.fn end end
assert(guarded)
B.values.native_configuration_v3={roamer_population=5};E.reset()
local function run(use_guard,slots)
 scratch.used=0;scratch.objects={};scratch.peak=0;scratch.restores=0
 local anchor=Vector3Box(vec(1,2,3));Script.set_temp_byte_count(0)
 local input={};for j=1,120 do input[j]={anchor} end
 local object=setmetatable({_nav_world={},_traverse_logic={},calls=0},{__index=NativeRoamer})
 function object:_random(a,b) self.calls=self.calls+1;return a end
 if use_guard then function object:_create_sub_zone_location(...) return guarded(NativeRoamer._create_sub_zone_location,self,...) end end
 local density={roamer_slot_placement_functions={"flood_fill"},roamer_slot_placement_settings={flood_fill={num_slots=slots}},shared_aggro_trigger=true}
 local zones,count=object:_create_sub_zones(input,density,7,slots*120)
 for _,zone in ipairs(zones) do for _,location in ipairs(zone) do
  assert(location.position==anchor and location.group_id==7 and location.shared_aggro_trigger)
  assert(#location.roamer_slots==slots)
  for i,row in ipairs(location.roamer_slots) do assert(row.position.coords[1]==i+1);assert(row.rotation.coords[3]==0) end
 end end
 return count,scratch.peak,scratch.used,object.calls,scratch.restores
end
for _,slots in ipairs({50,250,300}) do
 local count,peak,used,calls=run(false,slots)
 local fixed_count,fixed_peak,fixed_used,fixed_calls,restores=run(true,slots)
 assert(fixed_count==count and fixed_calls==calls and restores==121)
 assert(fixed_used==0 and fixed_peak*100<peak)
 memory_result={slots=slots,count=count,unscoped_peak=peak,scoped_peak=fixed_peak}
end
-- Preserve caller temporaries; default and remote sessions keep the native path.
local anchor=vec(9,8,7);local offset=Script.temp_byte_count()
local n=guarded(function() vec(1,1,1);return {boxed=true},4 end,{},nil,nil,nil)
assert(anchor.live and Script.temp_byte_count()==offset and n.boxed)
host=false;local previous=scratch.restores
guarded(function() return {},4 end,{},nil,nil,nil);assert(scratch.restores==previous)
host=true;B.values.native_configuration_v3={};E.reset()
guarded(function() return {},4 end,{},nil,nil,nil);assert(scratch.restores==previous)
""")
result={k:v for k,v in L.globals().memory_result.items()}
print('Actual flood-fill slot boxing and subzone placement: identical counts/RNG, valid boxed results, caller temporaries preserved, bounded scratch at high density:',result,'PASS')
