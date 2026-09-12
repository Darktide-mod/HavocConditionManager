"""Rear-only passive admission, native record lifetime and bounded backlog drain."""
import native_recycling_harness as h
from native_harness import *

# Execute the real cached progress getter. Geometry remains an explicit fixture.
L.execute('NativeLinear={};local PathTypeLinear=NativeLinear;'+h.method(
    'scripts/managers/main_path/path_types/path_type_linear.lua', 'PathTypeLinear', 'behind_unit'))
L.execute('''
function rear_setup()
 setup()
 route={_side_progress_on_path={[1]={behind_unit=players[1],behind_travel_distance=201,behind_path_position=Vector3Box(vec(201))}}}
 main.path_type=function() return "linear" end
 main.behind_unit=function(_,id) return NativeLinear.behind_unit(route,id) end
 main.travel_distance_from_position=function() error("passive recovery projected enemy position") end
end
function passive_roamer(x,progress)
 local u,r,ext=roaming("renegade_executor")
 POSITION_LOOKUP[u]=vec(x or 0);r.position=Vector3Box(vec(x or 0));r.travel_distance=progress or 0
 BLACKBOARDS[u].perception.aggro_state="passive"
 return u,r,ext
end
rear_setup();local u,r=passive_roamer();run(0,29)
assert(#deleted==0 and physics_queries==0)
tick(30);assert(#deleted==1 and deleted[1]==u and physics_queries==4)
assert(r._hcm_retired and r.active and not rp._roamer_lookup[u])
-- Actual native retirement unregisters now; queued engine deletion is later.
local called=0
assert(not deactivated(function() called=called+1;error("double passive despawn") end,rp,r))
assert(called==0 and r.active)
HEALTH_ALIVE[u]=false;ALIVE[u]=false
assert(deactivated(NativeRoamer._deactivate_roamer,rp,r) and rp._num_roamers==0)
finish_recovery(1)
print("Untouched native rear roamer: one 30-second timer, actual unregister, one credit and deferred passive-record cleanup without respawn/double despawn: PASS")

for _,guard in ipairs({"ahead","within_team","rear_59","moved","unknown_record","unknown_route","open_map","unknown_progress","invalid_progress","near_bot","cached_visible","fresh_visible","owner","objective","auto_event","invulnerable","spawner"}) do
 rear_setup();local u,r,ext=passive_roamer()
 if guard=="ahead" then r.travel_distance=300;POSITION_LOOKUP[u]=vec(300);r.position=Vector3Box(vec(300))
 elseif guard=="within_team" then route._side_progress_on_path[1].behind_travel_distance=-100
 elseif guard=="rear_59" then route._side_progress_on_path[1].behind_travel_distance=59
 elseif guard=="moved" then POSITION_LOOKUP[u]=vec(13)
 elseif guard=="unknown_record" then ext._hcm_straggler.record=nil
 elseif guard=="unknown_route" then main.ready=false
 elseif guard=="open_map" then main.path_type=function() return "open" end
 elseif guard=="unknown_progress" then route._side_progress_on_path[1].behind_travel_distance=nil
 elseif guard=="invalid_progress" then r.travel_distance=-math.huge
 elseif guard=="near_bot" then POSITION_LOOKUP[players[4]]=vec(34)
 elseif guard=="cached_visible" then ext._line_of_sight_lookup[players[2]]=true
 elseif guard=="fresh_visible" then u.visible[players[4]]=true
 elseif guard=="owner" then ms._minions_with_owners[u]=true
 elseif guard=="objective" then u.extensions.mission_objective_target_system._registered_objective="required"
 elseif guard=="auto_event" then BLACKBOARDS[u].group_data.owning_auto_event_id="required"
 elseif guard=="invulnerable" then u.invulnerable=true
 else BLACKBOARDS[u].spawn.is_exiting_spawner=true end
 run(0,75);assert(#deleted==0,"passive guard: "..guard)
 assert(projection_queries==0)
end
rear_setup();local u,r=passive_roamer();route._side_progress_on_path[1].behind_travel_distance=60
POSITION_LOOKUP[u]=vec(12);run(0,30);assert(#deleted==1,"inclusive rear/anchor boundaries")
-- A previously engaged enemy is not granted immunity by reverting to passive.
setup();local u=roaming();tick(0);BLACKBOARDS[u].perception.aggro_state="passive"
run(1,30);assert(#deleted==1)
-- A returning rear teammate cancels the ready request before actual removal.
rear_setup();local u,r,ext=passive_roamer();local update=ext.update
function ext:update(unit,dt,t)
 update(self,unit,dt,t)
 if t==30 then route._side_progress_on_path[1].behind_travel_distance=-50 end
end
run(0,30);assert(#deleted==0)
route._side_progress_on_path[1].behind_travel_distance=201
run(31,60);assert(#deleted==0);run(61,66);assert(#deleted==1)
print("Ahead/between-team/unknown/moved/open-map passive enemies stay; bots, visibility, damage state and ownership guards apply; returning team cancels at removal: PASS")

setup();for i=1,240 do roaming("renegade_executor") end
local before,rays,last=0,0,-1;local times={};local ready_peak=0
for step=0,380 do
 local t=step*.25;tick(t)
 ready_peak=math.max(ready_peak,recovery_state().ready_size)
 assert(recovery_state().ready_size<=64)
 assert(#deleted-before<=1 and physics_queries-rays<=4,"per-update burst")
 if #deleted>before then
  assert(last<0 or t-last>=.25,"rate limit")
  last=t;times[#times+1]=t
 end
 assert(projection_queries==0 and position_queries==0)
 before=#deleted;rays=physics_queries
end
assert(#deleted==240 and times[1]>=30 and times[240]<=95,"large rear backlog failed to drain")
for i=5,#times do assert(times[i]-times[i-4]>=1,"more than four removals in one second") end
assert(ready_peak>=63,"large backlog did not exercise the bounded ready ring")
finish_recovery(240)
print("240 eligible enemies: all retired by 95 seconds, four/sec maximum, one/update, <=four teammate LOS calls/update, bounded 64-slot ring and zero route queries: PASS")
setup();for i=1,100 do roaming() end;run(0,30)
local before=#deleted;tick(1000)
assert(#deleted-before<=1,"long frame caused catch-up burst")
print("Long frame never triggers a catch-up removal burst: PASS")
''')
