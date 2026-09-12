"""3.6.3 log regressions: stationary leftovers and native spawn throughput."""
import native_recycling_harness as h
from native_harness import *
method=h.method
def source(path): return (game/path).read_text(encoding='utf-8-sig')
L.execute("""
function find_hook(path,name)
 local target=type(path)=="string" and require(path) or path
 for _,h in ipairs(hooks) do if h.target==target and h.name==name then return h.fn end end
 error("hook unavailable: "..name)
end
NativeTerror={}
""")
for name in ('num_active_events','update','stop_terror_trickle'):
 L.execute('local TerrorEventManager=NativeTerror;'+method('scripts/managers/terror_event/terror_event_manager.lua','TerrorEventManager',name))
L.execute('local MinionSpawnManager=NativeMinion;'+method('scripts/managers/minion/minion_spawn_manager.lua','MinionSpawnManager','_register_minion_to_objective'))
L.execute('''
-- Objective UI/network registration is an engine boundary in this harness.
NativeObjective.setup_from_external=function(self,name)
 assert(name=="required");self._registered_objective=name
end
''')
# Execute actual native mission node, door queue and completion bookkeeping.
L.execute('NativeEventNodes={};NativeDoor={};NativeDoorQueue={};NativeDoorSystem={};NativeBreedQueries={}')
for owner,target,path,names,prefix in [
 ('MinionSpawnerQueue','NativeDoorQueue','scripts/extension_systems/minion_spawner/utilities/minion_spawner_queue.lua',('init','enqueue','dequeue','is_empty'),''),
 ('MinionSpawnerExtension','NativeDoor','scripts/extension_systems/minion_spawner/minion_spawner_extension.lua',('add_spawns','update','_spawn','is_spawning','request_param_table'),
  'local DEFAULT_SPAWN_DELAY=.25;local Breeds=require("scripts/settings/breed/breeds");local aggro_states={aggroed="aggroed"};'),
 ('MinionSpawnerSystem','NativeDoorSystem','scripts/extension_systems/minion_spawner/minion_spawner_system.lua',('spawners_in_group',),''),
 ('BreedQueries','NativeBreedQueries','scripts/utilities/breed_queries.lua',('add_spawns_single_breed',),''),
]:
    for name in names: L.execute('local '+owner+'='+target+';'+prefix+method(path,owner,name))
text=source('scripts/managers/terror_event/terror_event_nodes.lua')
start=text.index('TerrorEventNodes.spawn_by_points = {')
end=text.index('\nTerrorEventNodes.',start+1)
L.execute('''local TerrorEventNodes=NativeEventNodes;local BreedQueries=NativeBreedQueries
local MAX_TERROR_EVENT_THRESHOLD=100;local MAX_POINTS=60;local TEMP_SPAWN_SIDE_NAME="villains"
local GROUP_SOUNDS_BY_BREED_NAME={};local aggro_states={passive="passive",aggroed="aggroed"}
local MinionDifficultySettings={terror_event_point_costs={}}
'''+text[start:end])
L.execute('''
patrol_setup()
local engine=Managers.state.unit_spawner
local create_entity=engine.spawn_network_unit
engine.spawn_network_unit=function(self,...)
 local unit=create_entity(self,...)
 unit.extensions.behavior_system={behavior_state_event=function() end}
 return unit
end
pm._side_id=2;pm.roamer_traverse_logic=function() return "logic" end
pm.spawn_type_allowed=function() return true end
pm.num_aggroed_minions=function() return 0 end
pm.spawn_type_enabled=function() return false end
pm.get_ramp_up_frequency_modifier=function() return 1 end
Managers.state.difficulty.get_table_entry_by_resistance=function() return 1 end
Managers.state.terror_event={get_excluded_tags_replacement=function() end,get_tags_replacement=function() end,
 get_terror_event_point_modifier=function() return 1 end,get_max_points_modifer=function() return 1 end,
 _active_events={{}},_start_events={},_terror_trickle_data={active=false},num_active_events=NativeTerror.num_active_events}
function NativeBreedQueries.match_minions_by_tags() return {} end
function NativeBreedQueries.pick_random_minion_by_points(_,points) assert(points==8);return Breeds.renegade_executor,6 end
function table.shallow_copy(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
function table.set_readonly(t) return t end
function table.shuffle(t) return t end
Component={event=function(unit,name) unit.events[#unit.events+1]=name end}
MinionSpawnerSpawnPosition={validate_exit_position=function() return true end}
local original_spawn=ms.spawn_minion
ms.spawn_minion=function(self,...) return find_hook("scripts/managers/minion/minion_spawn_manager","spawn_minion")(original_spawn,self,...) end
local system=setmetatable({_spawner_group_extensions={}}, {__index=NativeDoorSystem})
function system:enable_update_function() end
function system:disable_update_function() end
local function door(x)
 local q=setmetatable({}, {__index=NativeDoorQueue});q:init()
 local unit={events={}};POSITION_LOOKUP[unit]=vec(x)
 local d=setmetatable({_unit=unit,_nav_world={},_traverse_logic="logic",_is_setup=true,_is_server=true,
  _spawn_queue=q,_spawned_minions_by_queue_id={},_owner_system=system,_exit_position=Vector3Box(vec(x)),
  _spawn_position=Vector3Box(vec(x)),_spawn_rotation=Vector3Box(vec(0))},{__index=NativeDoor})
 function d:exit_position_boxed() return self._exit_position end
 function d:add_spawns(...) return find_hook("scripts/extension_systems/minion_spawner/minion_spawner_extension","add_spawns")(NativeDoor.add_spawns,self,...) end
 function d:_spawn(...) return find_hook("scripts/extension_systems/minion_spawner/minion_spawner_extension","_spawn")(NativeDoor._spawn,self,...) end
 return d
end
local sewer,near_a,near_b=door(130),door(260),door(240)
system._spawner_group_extensions.spawner_ascender_trickle_a={sewer,near_a}
system._spawner_group_extensions.spawner_ascender_trickle_b={near_b}
system._spawner_group_extensions.spawner_ascender_trickle_c={}
sides.get_side_from_name=function(_,name) return name=="villains" and enemy_side or {side_id=1} end
enemy_side.relation_sides=function() return {{side_id=1}} end
local get_system=Managers.state.extension.system
Managers.state.extension.system=function(self,name) if name=="minion_spawner_system" then return system end;return get_system(self,name) end
local node={"spawn_by_points",points=8,spawner_group="spawner_ascender_trickle_a",breed_tags={{"elite"}},limit_spawners=3}
local scratch={spawned_minion_data={}}
local node_hook=find_hook(require("scripts/managers/terror_event/terror_event_nodes").spawn_by_points,"update")
node_hook(NativeEventNodes.spawn_by_points.update,node,scratch,0,.1)
assert(scratch.started_spawn,"native event was delayed by HCM")
local done
for frame=1,80 do
 now=frame*.1
 done=node_hook(NativeEventNodes.spawn_by_points.update,node,scratch,now,.1)
 for _,d in ipairs({sewer,near_a,near_b}) do NativeDoor.update(d,d._unit,.1,now) end
 for _,unit in ipairs(all_created) do BLACKBOARDS[unit].spawn.is_exiting_spawner=false end
end
assert(done and scratch.started_spawn and #all_created==6)
assert(#sewer._unit.events>0 and #near_b._unit.events==0,"authored event door pool was altered")
local accounted=0
for spawner,ids in pairs(scratch.spawned_minion_data.spawner_queue_id) do
 assert(spawner~=near_b)
 for _,id in ipairs(ids) do accounted=accounted+#spawner._spawned_minions_by_queue_id[id] end
end
assert(accounted==6 and node.spawner_group=="spawner_ascender_trickle_a" and node.points==8)
for _,u in ipairs(all_created) do
 local meta=u.extensions.perception_system._hcm_straggler
 assert(meta and not meta.protected)
 POSITION_LOOKUP[u]=vec(0)
end
run(10,60);assert(#deleted==6,"active non-objective event blocked out-of-contact cleanup")
Managers.state.terror_event._update_event=function() return true end
Managers.telemetry_events={stop_terror_event=function() end}
Managers.state.terror_event._active_events[1].name="completed_event"
Managers.state.terror_event._update_terror_trickle=function() end
NativeTerror.update(Managers.state.terror_event,.1,61)
assert(Managers.state.terror_event:num_active_events()==0)
run(61,105)
assert(#deleted==6,"completed event leftovers never retired")
finish_recovery(6)
assert(not B.current_spawn_batch)
local untouched=0
node.mission_objective_id="required"
assert(node_hook(function() untouched=untouched+1;return true end,node,{},now,.1) and untouched==1)
print("Actual ascender node: native door pool and timing; six actual entities and queue IDs; active non-objective event leftovers retired without waiting for completion: PASS")

local required={spawned_minion_data={}}
node_hook(NativeEventNodes.spawn_by_points.update,node,required,106,.1)
for frame=1,80 do
 now=106+frame*.1
 for _,d in ipairs({sewer,near_a,near_b}) do NativeDoor.update(d,d._unit,.1,now) end
end
assert(#all_created==12)
for i=7,12 do
 local u=all_created[i]
 assert(u.extensions.perception_system._hcm_straggler.protected,"required objective lost recorded ownership")
 POSITION_LOOKUP[u]=vec(0);BLACKBOARDS[u].spawn.is_exiting_spawner=false
end
run(115,180);assert(#deleted==6,"required objective retired after event end")
print("Native required-objective event: six additional entities remain excluded after event completion: PASS")

''')


L.execute('''
-- A native horde can queue more than one full ring. HCM must consume each
-- original request once without testing or moving its native position.
for _,count in ipairs({256,300}) do
 setup();spawn_visible=true
 local original=ms.spawn_minion;local consumed={}
 ms.spawn_minion=function(self,breed,position,rotation,side,params)
  consumed[#consumed+1]=params.request_id
  assert(position[1]==params.request_id,"native position was rewritten")
  return find_hook("scripts/managers/minion/minion_spawn_manager","spawn_minion")(original,self,breed,position,rotation,side,params)
 end
 ms.queue_minion_to_spawn=function(self,...)
  return find_hook("scripts/managers/minion/minion_spawn_manager","queue_minion_to_spawn")(NativeMinion.queue_minion_to_spawn,self,...)
 end
 local batch=B.new_spawn_batch("far_vector_horde",2,1);batch.horde=true;batch.kind="hordes"
 B.current_spawn_batch=batch
 for i=1,count do
  local entry=ms:queue_minion_to_spawn("renegade_executor",vec(i),Quaternion.identity(),2)
  entry.request_id=i
 end
 B.current_spawn_batch=nil
 assert(ms:total_allocated_num_enemies()==count)
 for i=1,count do ms:_update_spawn_queue();assert(#all_created==i and consumed[i]==i) end
 assert(ms._spawn_queue_size==0 and #all_created==count and position_queries==0 and spawn_los_queries==0)
end
assert(not B.spawn_navigation and not B.spawn_placement.route and not B.prepare_horde_entry)
print("Native full/expanded spawn rings: 256/300 original requests and positions consumed exactly once, zero placement/path/LOS admission work: PASS")

setup();local original=ms.spawn_minion
ms.spawn_minion=function(self,...)
 return find_hook("scripts/managers/minion/minion_spawn_manager","spawn_minion")(original,self,...)
end
pm.spawn_type_enabled=function() return pm.allowed end
local batch=B.new_spawn_batch("flood_horde",2,1);batch.horde=true;batch.kind="hordes"
local entry=ms:queue_minion_to_spawn("renegade_executor",vec(0),Quaternion.identity(),2)
entry._hcm_batch=batch;entry.spawn_source="horde";entry.optional_aggro_state="aggroed"
ms:_update_spawn_queue();local initial=all_created[1]
BLACKBOARDS[initial].group_data.group_target=players[1]
run(0,35);assert(#deleted==1)
pm.allowed=true;run(36,45);ms:_update_spawn_queue()
assert(#all_created==2 and BLACKBOARDS[all_created[2]].spawn.spawn_source=="hcm_redeployed")
POSITION_LOOKUP[all_created[2]]=vec(0);pm.allowed=false
run(46,90);assert(#deleted==2)
finish_recovery(0)
print("Ordinary horde with retained group target: native creation -> retirement -> one actual replacement -> second retirement without another credit: PASS")
''')
