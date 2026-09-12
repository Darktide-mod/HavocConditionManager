"""Simple out-of-contact recovery and native lifetime/queue regressions."""
import native_recycling_harness as h
from native_harness import *
L.execute('''
setup();local u,r,ext=roaming("renegade_executor")
assert(not E.config().changed,"test must exercise default level")
run(0,29);assert(#deleted==0 and physics_queries==0)
tick(30);assert(#deleted==1 and deleted[1]==u and physics_queries==4)
assert(ms._num_spawned_minions==0 and pm._total_challenge_rating==0 and pm._num_aggroed_minions==0)
assert(not rp._roamer_lookup[u] and r._hcm_retired and r.active)
-- Engine deletion completes asynchronously; the original dead-record consumer
-- removes the record rather than respawning the old encounter.
HEALTH_ALIVE[u]=false;ALIVE[u]=false
assert(deactivated(NativeRoamer._deactivate_roamer,rp,r))
assert(rp._num_roamers==0 and #rp._roamers==0)
run(31,45);assert(ms._spawn_queue_size==0 and position_queries==0,"paused pacing spawned replacement")
pm.allowed=true;tick(46);assert(ms._spawn_queue_size==1 and ms:total_allocated_num_enemies()==1)
ms:_update_spawn_queue();assert(ms._spawn_queue_size==0 and ms._num_spawned_minions==1)
local replacement=all_created[2]
assert(BLACKBOARDS[replacement].spawn.spawn_source=="hcm_redeployed")
assert(replacement.extensions.unit_data_system:breed().name=="renegade_executor")
assert(replacement.extensions.perception_system._hcm_straggler and not replacement.extensions.perception_system._hcm_straggler.record)
POSITION_LOOKUP[replacement]=vec(0);run(47,90)
assert(#deleted==2 and #all_created==2 and ms._spawn_queue_size==0,"replacement produced a second credit")
finish_recovery(0)
print("Native default-level perception -> release of entity/aggro/roamer record -> deferred queue -> actual creation -> no repeat credit: PASS")
print("Actual native objective component init and registrar: unassigned default objective permits rear recycling: PASS")


for _,guard in ipairs({"passive","visible","near_bot","damage","objective","owner","automatic_controller","invulnerable","spawner","client"}) do
 setup();local u=roaming("renegade_executor")
 if guard=="passive" then BLACKBOARDS[u].perception.aggro_state="passive"
 elseif guard=="visible" then u.extensions.perception_system._line_of_sight_lookup[players[1]]=true
 elseif guard=="near_bot" then POSITION_LOOKUP[players[4]]=vec(30)
 elseif guard=="damage" then u.ongoing_damage=true
 elseif guard=="objective" then u.extensions.mission_objective_target_system._registered_objective="required"
 elseif guard=="owner" then ms._minions_with_owners[u]=true
 elseif guard=="automatic_controller" then BLACKBOARDS[u].group_data.owning_auto_event_id="required"
 elseif guard=="invulnerable" then u.invulnerable=true
 elseif guard=="spawner" then BLACKBOARDS[u].spawn.is_exiting_spawner=true
 else host=false end
 run(0,150);assert(#deleted==0 and physics_queries==0,"guard: "..guard)
end
for _,breed in ipairs({"renegade_flamer","chaos_spawn","renegade_captain"}) do
 setup();roaming(breed);run(0,150);assert(#deleted==0)
end
setup();local u=roaming();u.visible[players[4]]=true;run(0,35)
assert(#deleted==0 and physics_queries==4,"fresh player visibility was skipped")
print("Unverified ambient enemies, visibility, every teammate including bots, actual damage, objectives/ownership and protected enemy types: PASS")

for _,trace in ipairs({"stationary","moving","looping","no_route","smart_object","stale_effects","unknown_origin"}) do
 setup();local u=roaming("renegade_executor")
 main.travel_distance_from_position=function() error("recovery used route projection") end
 u.extensions.navigation_system.remaining_distance_from_progress_to_end_of_path=function() error("recovery queried navigation") end
 if trace=="moving" then u.test_motion=function(t) return vec(t*.2) end
 elseif trace=="looping" then u.test_motion=function(t) return vec(t%20<10 and 0 or 10) end
 elseif trace=="no_route" then main.ready=false
 elseif trace=="smart_object" then u.traversing=true
 elseif trace=="stale_effects" then u.tagged=1;u.keywords.weapon_malfunction=true;u.keywords.bleeding=true
 elseif trace=="unknown_origin" then BLACKBOARDS[u].spawn.spawn_source="native_other" end
 run(0,40);assert(#deleted==1,"out-of-contact rule: "..trace)
end
setup();local u=roaming();run(0,20);u.ongoing_damage=true;tick(21);u.ongoing_damage=nil
run(22,50);assert(#deleted==0);run(51,56);assert(#deleted==1,"damage imposed two grace periods")
print("One 30-second rule: stationary/moving/looping/no-route/traversal/stale marks and effects/other origins recover; renewed damage restarts only one timer: PASS")

for _,case in ipairs({"one_active","passive_patrol","locked_group"}) do
 patrol_setup();local group=boss_patrol(12)
 if case=="one_active" then POSITION_LOOKUP[group.members[12]]=vec(190)
 elseif case=="locked_group" then gs:lock_group_id(group.id) end
 run(0,110)
 assert(#deleted==(case=="one_active" and 11 or 12),case)
end
patrol_setup();trickle_patrol();run(0,80);assert(#deleted==6)
for _,params in ipairs({{externally_controlled_patrol=true},{mutator_name="mission"}}) do
 patrol_setup();trickle_patrol(params);run(0,100);assert(#deleted==0)
end
print("Known passive and combat patrols retire per member; active member stays; native groups and controlled patrol ownership remain valid: PASS")

setup();for i=1,300 do roaming() end
for step=0,480 do tick(step*.25) end;assert(#deleted==300)
finish_recovery(256)
setup();for i=1,240 do roaming() end
local prior_removed,prior_rays=0,0
for t=0,350 do
 tick(t)
 assert(#deleted-prior_removed<=1 and physics_queries-prior_rays<=4)
 assert(projection_queries==0,"retirement projected a route")
 prior_removed=#deleted;prior_rays=physics_queries
end
assert(#deleted==240 and native_ticks==240*351)
finish_recovery(240)
print("300 retirements retain a bounded 256-unit allowance; 240 fit without expiry or discard; at most one removal/four final LOS calls per update in the 1 Hz fixture and zero route queries: PASS")
''')
L.execute('''
-- Native queue consumption must recheck the *current* team, including a bot.
-- Refusals clear only this request and return its unit to the finite credit.
for _,reason in ipairs({"player_moved","visible_now","safe_zone","pacing_pause"}) do
 setup();roaming();run(0,30);pm.allowed=true;tick(38)
 assert(ms._spawn_queue_size==1 and #all_created==1)
 if reason=="player_moved" then
  POSITION_LOOKUP[players[4]]=vec(248);enemy_side.valid_enemy_player_units_positions[4]=POSITION_LOOKUP[players[4]]
 elseif reason=="visible_now" then spawn_visible=true
 elseif reason=="safe_zone" then pm.safe=true
 else pm.allowed=false end
 ms:_update_spawn_queue()
 assert(ms._spawn_queue_size==0 and #all_created==1,"stale request escaped dequeue guard: "..reason)
 POSITION_LOOKUP[players[4]]=vec(204);enemy_side.valid_enemy_player_units_positions[4]=POSITION_LOOKUP[players[4]]
 spawn_visible=false;pm.safe=false;pm.allowed=true
 tick(46);assert(ms._spawn_queue_size==1)
 ms:_update_spawn_queue();assert(#all_created==2 and ms._spawn_queue_size==0)
 finish_recovery(0)
end
-- An accepted credit still exists after a long native queue delay. Current
-- placement and local-session ownership remain mandatory at consumption.
setup();roaming();run(0,30);pm.allowed=true;tick(38);now=211
ms:_update_spawn_queue();assert(#all_created==2 and ms._spawn_queue_size==0)
tick(219);finish_recovery(0)
setup();roaming();run(0,30);pm.allowed=true;tick(38);B.finish_straggler_recycling()
ms:_update_spawn_queue();assert(#all_created==1 and ms._spawn_queue_size==0)
print("Actual native dequeue: moved teammate, fresh visibility, safe zone, pacing pause, long wait and reset; retry preserves exactly one credit: PASS")
''')
