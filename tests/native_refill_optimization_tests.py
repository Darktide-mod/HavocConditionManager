"""Native refill fairness, mission-lifetime allowances and local mesh candidates."""
import native_recycling_harness as h
from native_harness import *

L.execute("""
function refill_setup()
 patrol_setup();pm.allowed=false;queue_spawning=true
end
function drain_at(t)
 now=t;B.update_straggler_recycling(pm,t);ms:_update_spawn_queue()
end
-- The log's 103 earned credits must survive waiting beyond the old 180s TTL.
refill_setup()
for i=1,103 do roaming("renegade_executor") end
for step=0,320 do tick(step*.25) end
assert(#deleted==103 and #all_created==103 and position_queries==0)
now=300;pm.allowed=true
local previous=103;local first,last;local times={}
for step=0,120 do
 local t=300+step*.25;drain_at(t)
 assert(#all_created-previous<=1 and ms._spawn_queue_size==0)
 if #all_created>previous then
  first=first or t;last=t;times[#times+1]=t
 end
 previous=#all_created
end
assert(#all_created==206 and ms._num_spawned_minions==103,"accepted credits expired or stalled")
assert(last-first<=26,"eight-second batch gaps remain")
for i=2,#times do assert(times[i]-times[i-1]>=.25) end
for _,group in pairs(gs._groups) do assert(not gs._locked_group_ids[group.id],"completed refill group locked") end
finish_recovery(0)
print("103 native earned credits wait beyond 180 seconds, then all 103 recreate within 26 seconds once placement/capacity permit; no batch gaps or rate bursts: PASS")

-- Fair selection must pass a paused first class and remove the exact completed
-- credit rather than deleting an unrelated head record.
refill_setup()
local a=roaming("chaos_poxwalker");a.extensions.perception_system._hcm_straggler.kind="roamers"
run(0,30);assert(#deleted==1)
local b=roaming("renegade_executor");b.extensions.perception_system._hcm_straggler.kind="monsters"
run(31,61);assert(#deleted==2)
local c=roaming("chaos_ogryn_executor");c.extensions.perception_system._hcm_straggler.kind="trickle_hordes"
run(62,92);assert(#deleted==3)
function pm:spawn_type_enabled(kind) return kind~="roamers" end
for step=0,12 do drain_at(100+step*.25) end
assert(#all_created==5)
assert(all_created[4].extensions.unit_data_system:breed().name=="renegade_executor")
assert(all_created[5].extensions.unit_data_system:breed().name=="chaos_ogryn_executor")
function pm:spawn_type_enabled() return true end
for step=0,8 do drain_at(104+step*.25) end
assert(#all_created==6 and all_created[6].extensions.unit_data_system:breed().name=="chaos_poxwalker")
finish_recovery(0)
print("Paused head class cannot block two ready classes; non-head completions preserve the paused credit and all three native breeds recreate exactly once: PASS")

-- One in-flight request globally even when another credit is runnable.
-- Cancel a non-head ticket; both its allowance and group remain retryable.
refill_setup()
local a=roaming("chaos_poxwalker");a.extensions.perception_system._hcm_straggler.kind="roamers"
run(0,30);assert(#deleted==1)
for i=1,2 do local u=roaming("renegade_executor");u.extensions.perception_system._hcm_straggler.kind="monsters" end
run(31,66);assert(#deleted==3)
for i=1,2 do local u=roaming("chaos_ogryn_executor");u.extensions.perception_system._hcm_straggler.kind="trickle_hordes" end
run(67,102);assert(#deleted==5)
function pm:spawn_type_enabled(kind) return kind~="roamers" end
now=120;B.update_straggler_recycling(pm,now)
assert(ms._spawn_queue_size==1)
for step=1,16 do now=120+step*.25;B.update_straggler_recycling(pm,now);assert(ms._spawn_queue_size==1) end
placement_live_valid=false;ms:_update_spawn_queue()
assert(#all_created==5 and ms._spawn_queue_size==0)
placement_live_valid=true
for step=0,40 do drain_at(125+step*.25) end
assert(#all_created==9)
function pm:spawn_type_enabled() return true end
for step=0,8 do drain_at(136+step*.25) end
assert(#all_created==10)
finish_recovery(0)
print("Global one-inflight bound, non-head cancellation, retry and native group completion retain every allowance exactly once: PASS")

-- Capacity remains authoritative; releasing it can use the retained credits.
refill_setup();roaming();run(0,35);pm.allowed=true
local allocated=ms.total_allocated_num_enemies
ms.total_allocated_num_enemies=function() return 10000 end
local before=placement_engine.created
for step=0,100 do drain_at(300+step*.25) end
assert(#all_created==1 and placement_engine.created==before)
ms.total_allocated_num_enemies=allocated
for step=0,8 do drain_at(327+step*.25) end
assert(#all_created==2)
finish_recovery(0)
print("Native capacity pressure preserves accepted allowance and performs no placement search while full: PASS")
""")

L.execute("""
local Placement=B.spawn_placement
local points=require("scripts/managers/main_path/utilities/spawn_point_queries")
function local_setup()
 refill_setup();pm.allowed=true
 PhysicsWorld.raycast=function() return true end
 points.get_occluded_positions=function() return {},0 end
end
local_setup()
for i,player in ipairs(players) do
 POSITION_LOOKUP[player]=vec(200+i,0,12)
 enemy_side.valid_enemy_player_units_positions[i]=POSITION_LOOKUP[player]
end
placement_plan=function(from,to)
 assert(to[3]==12 and from[3]==12,"local sample projected to the wrong floor")
 return {}
end
now=0;local context=Placement.context(2,1,0);context.prefer_near=true
local anchor=Placement.anchor(context)
assert(anchor and anchor[3]==12 and #placement_engine.starts==1)
for _,player in ipairs(players) do assert(Vector3.distance(anchor,POSITION_LOOKUP[player])>=20) end
assert(Placement.valid(context,anchor))
print("No authored hidden points: bounded local mesh candidates produce a hidden same-floor anchor with a complete enemy-to-player route before spawning: PASS")

-- A local mesh point is only a candidate, never permission to skip direction,
-- actual LOS, native path validity, connected footprint or async completion.
local_setup();placement_plan=function() return {found=false} end
local mesh_samples=0
placement_floor=function(position)
 if Vector3.distance_squared(position,POSITION_LOOKUP[players[1]])>20*20 then mesh_samples=mesh_samples+1 end
 return vec(position[1],position[2],position[3])
end
for step=0,160 do now=step*.25;local c=Placement.context(2,1,now);c.prefer_near=true;assert(not Placement.anchor(c)) end
assert(#all_created==0 and #placement_engine.starts<=41)
Placement.finish()
assert(mesh_samples>0 and mesh_samples<=8*(math.floor(40/4)+1),"unbounded local mesh work")

local_setup();placement_plan=function() return {done=false} end
now=0;context=Placement.context(2,1,now);context.prefer_near=true
assert(not Placement.anchor(context))
local projections=placement_engine.projections
for step=1,240 do now=step/60;local c=Placement.context(2,1,now);c.prefer_near=true;assert(not Placement.anchor(c)) end
assert(#placement_engine.starts==1 and placement_engine.projections==projections and placement_engine.polls<=18)
local handle=placement_engine.handles[1];handle.done=true
now=5;context=Placement.context(2,1,now);context.prefer_near=true
assert(Placement.anchor(context))
PhysicsWorld.raycast=function() return false end
assert(not Placement.valid(context,handle and vec(229)))
Placement.finish()
print("Local candidates still reject failed native routes and visible positions; delayed route work stays one shared query without repeated local scans: PASS")
""")
