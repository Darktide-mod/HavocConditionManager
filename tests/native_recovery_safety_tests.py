"""No-debug runtime, last-moment safety and batched replacements."""
import native_recycling_harness as h
from native_harness import *
L.execute('''
for _,reason in ipairs({"near_teammate","objective_or_controller","fresh_visibility"}) do
 setup();lines={};local u=roaming("renegade_executor")
 u.extensions.navigation_system._enabled=false;u.extensions.navigation_system._is_using_smart_object=true
 u.extensions.navigation_system.is_following_path=function() error("debug navigation query") end
 main.travel_distance_from_position=function() error("debug route query") end
 if reason=="near_teammate" then POSITION_LOOKUP[players[4]]=vec(20)
 elseif reason=="objective_or_controller" then u.extensions.mission_objective_target_system._registered_objective="required"
 else u.visible[players[1]]=true end
 run(0,90);assert(#deleted==0)
 B.finish_straggler_recycling()
 assert(#lines==0,"blocked recovery emitted diagnostics")
end
print("Blocked recovery keeps teammate, objective and fresh-visibility guards with no diagnostics or route/navigation queries: PASS")

setup();lines={};POSITION_LOOKUP[players[4]]=vec(20)
for i=1,240 do roaming("renegade_executor") end
local box=Vector3Box;local boxes=0
Vector3Box=function(...) boxes=boxes+1;return box(...) end
run(0,900)
Vector3Box=box
B.finish_straggler_recycling();B.finish_spawn_tracking();B.finish_spawn_flow();B.spawn_placement.finish()
assert(#deleted==0 and #lines==0 and boxes==0 and projection_queries==0 and physics_queries==0)
print("240 continuously blocked enemies over 900 seconds: zero diagnostic output including mission cleanup, no box allocation or added ray/path queries: PASS")

for _,late in ipairs({"near_bot","damage","visible"}) do
 setup();local u,_,ext=roaming("renegade_executor")
 local update=ext.update
 function ext:update(unit,dt,t)
  update(self,unit,dt,t)
  if t==30 then
   if late=="near_bot" then POSITION_LOOKUP[players[4]]=vec(20)
   elseif late=="visible" then u.visible[players[1]]=true
   else
    for _,hook in ipairs(hooks) do
     if hook.target==require("scripts/extension_systems/health/health_extension") and hook.name=="add_damage" then hook.fn({_unit=u},1) end
    end
   end
  end
 end
 run(0,30);assert(#deleted==0,"last-moment "..late.." ignored")
end
print("Ready-queue consumption rechecks a returning bot, renewed damage and actual visibility: PASS")

setup();pm.spawn_type_enabled=function() return false end
Managers.state.terror_event={num_active_events=function() error("recovery polled global event liveness") end}
local params=ms:request_param_table();params.optional_aggro_state="aggroed";params.spawn_source="unlisted_native_source"
local generic=ms:spawn_minion("renegade_executor",vec(0),Quaternion.identity(),2,params)
assert(generic.extensions.perception_system._hcm_straggler)
run(0,40);assert(#deleted==1 and deleted[1]==generic)
print("Generic native creation is tracked without a source whitelist or global event poll: PASS")

patrol_setup();local group=trickle_patrol();run(0,80);assert(#deleted==6)
pm.allowed=true;queue_spawning=true;now=86;B.update_straggler_recycling(pm,now)
assert(ms._spawn_queue_size==1)
for i=1,6 do
 ms:_update_spawn_queue()
 if i<6 then now=86+i*.25;B.update_straggler_recycling(pm,now);assert(ms._spawn_queue_size==1) end
end
queue_spawning=nil
assert(#all_created==12)
local replacement_group=gs._groups[1];assert(#replacement_group.members==6)
for _,u in ipairs(replacement_group.members) do
 assert(u.health_modifier==1.5 and BLACKBOARDS[u].spawn.spawn_source=="hcm_redeployed")
 POSITION_LOOKUP[u]=vec(0)
end
pm.allowed=false;run(88,180);assert(#deleted==12 and ms._spawn_queue_size==0)
finish_recovery(0)
print("Six separate retirements coalesce into one finite native batch; all six recreate with original breed/health, group closes, replacements earn no second credit: PASS")
''')
