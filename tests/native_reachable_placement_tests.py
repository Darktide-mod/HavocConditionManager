"""Pre-spawn directional reachability, incomplete routes and near fallback.

Uses the actual native minion creation, group lifetime and deferred queue.
Engine AStar/mesh/physics are explicit boundaries, not a real-map navmesh test.
"""
import native_recycling_harness as h
from native_harness import *
L.execute('local RoamerPacing=NativeRoamer;'+h.method(
    'scripts/managers/pacing/roamer_pacing/roamer_pacing.lua','RoamerPacing','destroy'))

L.execute("""
local Placement=B.spawn_placement
local points=require("scripts/managers/main_path/utilities/spawn_point_queries")
function placement_setup()
 patrol_setup();pm.allowed=true;queue_spawning=true
 PhysicsWorld.raycast=function() return true end
 far_points={vec(261),vec(270)};near_points={vec(232),vec(226)}
 points.get_occluded_positions=function(nav,all,origin,players,range,groups,minimum,maximum,initial,forward)
  assert(range==4 and groups==40)
  if minimum==35 then assert(maximum==120 and forward);return far_points,#far_points end
  assert(minimum==20 and maximum==60 and initial==4 and not forward)
  return near_points,#near_points
 end
 GwNavQueries.flood_fill_from_position=function(_,pos,a,b,n,output)
  for i=1,n do output[i]=vec(pos[1]+i*.25,pos[2],pos[3]) end;return n
 end
 main.ahead_unit=function() return players[1],POSITION_LOOKUP[players[1]][1],vec(POSITION_LOOKUP[players[1]][1]) end
end
function crusher_job()
 local breeds={};for i=1,21 do breeds[i]="chaos_ogryn_executor" end
 local record={breed_list={test={challenge_templates={breeds}}}}
 local manager={_nav_world=pm._nav_world,_pacing_type="default"}
 return manager,B.queue_native_patrol(manager,record,2,{groups={}})
end
function step_job(manager,t) now=t;B.update_patrol_spawns(manager,t,2,1) end
function context(t) now=t;return Placement.context(2,1,t) end

-- The reported pattern: a far point is disconnected; another has a nominal
-- but incomplete path; a nearer point has a complete native path.
placement_setup()
Managers.state.terror_event={num_active_events=function() error("unrelated active event was polled") end}
placement_plan=function(from,to)
 assert(to[1]==201,"path checked towards main-path ahead instead of the real player")
 if from[1]>265 then return {goal=vec(to[1]+20)} end
 if from[1]>250 then return {found=false} end
 return {}
end
local manager,job=crusher_job()
for frame=0,19 do step_job(manager,frame*.05);assert(#all_created==0,"created before a successful route") end
for frame=20,39 do step_job(manager,frame*.05);assert(#all_created==0,"incomplete path was treated as executable") end
for frame=40,180 do step_job(manager,frame*.05);if job.completed then break end end
assert(job.completed and #all_created==21 and #placement_engine.starts==3)
for _,unit in ipairs(all_created) do
 assert(unit.extensions.unit_data_system:breed().name=="chaos_ogryn_executor")
 assert(POSITION_LOOKUP[unit][1]>=232 and POSITION_LOOKUP[unit][1]<240)
 assert(BLACKBOARDS[unit].perception.aggro_state=="aggroed")
 for _,player in ipairs(players) do assert(Vector3.distance(POSITION_LOOKUP[unit],POSITION_LOOKUP[player])>=20) end
end
assert(not gs._locked_group_ids[job.group_id])
Placement.finish()
assert(placement_engine.created==1 and placement_engine.destroyed==1 and placement_engine.live_created==1 and placement_engine.live_destroyed==1)
assert(#lines==0)
print("Actual 21-crusher formation: disconnected far point and incomplete route rejected before creation; nearer walking route accepted, all 21 arrive through native creation with one shared query object: PASS")

-- Slow engine search: even repeated consumers/frames cannot create enemies
-- or start a second search until the single outstanding request completes.
placement_setup();placement_plan=function() return {done=false} end
manager,job=crusher_job()
for frame=0,120 do
 local t=frame/60;step_job(manager,t)
 Placement.anchor(context(t),{});Placement.anchor(context(t),{})
 assert(#all_created==0 and #placement_engine.starts==1)
end
assert(placement_engine.polls<=9,"pending search polled more than four times per second")
placement_engine.handles[1].done=true
for frame=121,170 do step_job(manager,frame/60);if #all_created>0 then break end end
assert(#all_created>0 and #placement_engine.starts==1)
B.finish_patrol_spawns(manager);Placement.finish()
print("Delayed route completion: zero speculative spawns, one shared in-flight query, bounded polling, no blocking game-thread wait: PASS")

-- Nearby means physically close and hidden, not forced ahead. A point behind
-- the team is allowed when its enemy-to-player path succeeds.
placement_setup();far_points={vec(261)};near_points={vec(171)}
placement_plan=function(from,to)
 assert(to[1]==201)
 return {found=from[1]<200}
end
assert(not Placement.anchor(context(0)))
local nearby=Placement.anchor(context(1))
assert(nearby and nearby[1]==171 and #placement_engine.starts==2)
assert(Placement.valid(context(1),vec(172)))
POSITION_LOOKUP[players[4]]=vec(181);enemy_side.valid_enemy_player_units_positions[4]=POSITION_LOOKUP[players[4]]
assert(not Placement.valid(context(1.1),vec(172)),"nearby spawn within 20m of a bot")
POSITION_LOOKUP[players[4]]=vec(204);enemy_side.valid_enemy_player_units_positions[4]=POSITION_LOOKUP[players[4]]
PhysicsWorld.raycast=function() return false end
assert(not Placement.valid(context(1.2),vec(172)),"nearby spawn in current player LOS")
print("Near fallback can use a reachable side/rear point; live LOS and 20m minimum from every teammate still apply: PASS")

-- Real player floor is the path endpoint. A different storey projected onto
-- the main path must not supply the patrol's destination.
placement_setup()
for i,player in ipairs(players) do
 POSITION_LOOKUP[player]=vec(200+i,0,12.5);enemy_side.valid_enemy_player_units_positions[i]=POSITION_LOOKUP[player]
end
far_points={vec(261,0,12)};near_points={}
placement_floor=function(p) return vec(p[1],p[2],12) end
placement_plan=function(from,to) assert(from[3]==12 and to[3]==12);return {} end
local record={breed_list={test={challenge_templates={{"chaos_ogryn_executor"}}}}}
manager={_nav_world=pm._nav_world,_pacing_type="default"};job=B.queue_native_patrol(manager,record,2)
step_job(manager,0)
assert(job.completed and BLACKBOARDS[all_created[1]].patrol.walk_position:unbox()[3]==12,
 string.format("floor fixture: created %d; paths %d; job next %.2f",#all_created,#placement_engine.starts,job.next_at))
local _,_,main_floor=main:ahead_unit(1)
assert(placement_engine.starts[1].to:unbox()[3]~=main_floor[3])
print("Stacked-floor fixture: AStar and passive patrol destination use the real player's projected floor: PASS")

-- A dynamic invalidation, a jump to another floor or a disconnected spread
-- point cannot inherit permission from a formerly successful anchor.
placement_setup();local anchor=Placement.anchor(context(0));assert(anchor)
placement_live_valid=false
assert(not Placement.valid(context(.1),vec(261.5)))
placement_live_valid=true
placement_ray_handler=function(from,to) return math.abs(from[3]-to[3])<1 and from[1]~=262 end
assert(not Placement.valid(context(.2),vec(262)),"island in flood-fill accepted")
POSITION_LOOKUP[players[1]]=vec(201,0,6);enemy_side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP[players[1]]
assert(not Placement.valid(context(.3),vec(261.5)),"cached endpoint crossed a storey")
POSITION_LOOKUP[players[1]]=vec(216);enemy_side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP[players[1]]
assert(not Placement.valid(context(.4),vec(261.5)),"large player movement retained old permission")
print("Live path invalidation, disconnected formation positions, target floor change and player movement reject stale permissions: PASS")

-- Final native dequeue must refuse a path that became invalid after enqueue,
-- preserving the finite replacement credit for another eligible point.
placement_setup();pm.allowed=false;roaming("renegade_executor")
run(0,35);assert(#deleted==1)
pm.allowed=true;now=40;B.update_straggler_recycling(pm,now)
assert(ms._spawn_queue_size==1)
placement_live_valid=false;ms:_update_spawn_queue()
assert(ms._spawn_queue_size==0 and #all_created==1)
finish_recovery(1)
print("Actual native queue consumption: route closes after enqueue, creation is cancelled and one replacement credit is retained: PASS")

-- A successful but partial path is also a refusal. Repeated failures have a
-- global start-rate limit and only one engine handle, including two consumers.
placement_setup();placement_plan=function(from,to) return {goal=vec(to[1]+20)} end
for frame=0,3600 do
 local t=frame/60
 assert(not Placement.anchor(context(t),{}))
 assert(not Placement.anchor(context(t),{}))
end
for i=2,#placement_engine.starts do
 assert(placement_engine.starts[i].t-placement_engine.starts[i-1].t>=1-1e-9)
end
assert(placement_engine.created==1 and placement_engine.live_created==1 and #placement_engine.starts<=61)
Placement.finish()
assert(placement_engine.destroyed==1 and placement_engine.live_destroyed==1)
placement_setup();placement_floor=function() return nil end
manager,job=crusher_job()
for t=0,20 do step_job(manager,t) end
assert(#all_created==0 and #placement_engine.starts==0)
B.finish_patrol_spawns(manager);Placement.finish()
print("Incomplete/missing navigation fails closed; concurrent callers share <=1 search start/second and all navigation handles are released: PASS")
placement_setup();placement_plan=function() return {done=false} end
assert(not Placement.anchor(context(0)))
local destroy_hook
for _,item in ipairs(hooks) do
 if item.target==require("scripts/managers/pacing/roamer_pacing/roamer_pacing") and item.name=="destroy" then destroy_hook=item.fn end
end
assert(destroy_hook)
local released_rules=false
GwNavTraverseLogic={destroy=function(rules)
 assert(rules==placement_traverse)
 assert(placement_engine.destroyed==1 and placement_engine.live_destroyed==1,"borrowed rules released before pending search")
 released_rules=true
end}
destroy_hook(NativeRoamer.destroy,{_traverse_logic=placement_traverse})
assert(released_rules);Placement.finish()
assert(placement_engine.destroyed==1 and placement_engine.live_destroyed==1)
print("Actual native Roamer.destroy: pending placement query and live path are released before their borrowed traversal rules; repeated cleanup is safe: PASS")
""")
