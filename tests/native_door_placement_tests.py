"""Native path authority without HCM door checks; actual queue creation.

The AStar path result and animation/navigation engine remain explicit boundaries.
These fixtures prove the Lua policy, not a particular mission door's authoring.
"""
import re
import subprocess
import native_recycling_harness as h
from native_harness import *


def native(path):
    source = GAME / path
    return source.read_text(encoding='utf-8-sig') if source.is_file() else subprocess.check_output(
        ['git', '-c', 'gc.auto=0', 'show', 'HEAD:' + path], cwd=GAME).decode('utf-8-sig')


def methods(path, owner, target, names, prefix=''):
    source = native(path)
    for name in names:
        body = re.search(r'^' + owner + r'\.' + name + r' = function\b.*?^end$', source, re.M | re.S)
        assert body, (path, name)
        L.execute('local ' + owner + '=' + target + ';' + prefix + body.group(0))


L.execute('NativeDoor={};NativeDoorAction={};NativeGraph={};NativeGraphSystem={};NativeGraphComponent={};NativePanel={}')
settings = lua_file(GAME / 'scripts/settings/components/door_settings.lua')
L.globals().NativeDoorSettings = settings
methods('scripts/extension_systems/door/door_extension.lua', 'DoorExtension', 'NativeDoor',
        ('can_open', 'nav_blocked', 'open', '_get_open_state_from_interactor'),
        'local STATES=NativeDoorSettings.STATES;local TYPES=NativeDoorSettings.TYPES;local OPEN_TYPES=NativeDoorSettings.OPEN_TYPES;')
methods('scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua', 'BtOpenDoorAction', 'NativeDoorAction',
        ('run',), 'local Blackboard=Blackboard;local DEFAULT_DOOR_OPEN_TIME_OFFSET=.2;local DEFAULT_OPEN_DOOR_ANIM_EVENT="idle";')
methods('scripts/extension_systems/nav_graph/nav_graph_extension.lua', 'NavGraphExtension', 'NativeGraph',
        ('unit', 'nav_graph_added', 'add_nav_graphs_to_database', 'remove_nav_graphs_from_database'))
methods('scripts/extension_systems/nav_graph/nav_graph_system.lua', 'NavGraphSystem', 'NativeGraphSystem',
        ('unit_from_smart_object_id', 'register_smart_object_id_to_extension'))
methods('scripts/components/nav_graph.lua', 'NavGraph', 'NativeGraphComponent', ('flow_nav_enable', 'flow_nav_disable'))
methods('scripts/extension_systems/door_control_panel/door_control_panel_extension.lua', 'DoorControlPanelExtension', 'NativePanel', ('is_active',),
        'local STATES={active="active",inactive="inactive"};')

L.execute("""
local Placement=B.spawn_placement
local points=require("scripts/managers/main_path/utilities/spawn_point_queries")

function door_setup()
 patrol_setup();pm.allowed=true;queue_spawning=true
 PhysicsWorld.raycast=function() return true end
 points.get_occluded_positions=function(_,_,_,_,_,_,minimum) if minimum==35 then return {vec(261)},1 end;return {},0 end
 GwNavQueries.flood_fill_from_position=function(_,pos,a,b,n,output)
  for i=1,n do output[i]=vec(pos[1]+i*.25,pos[2],pos[3]) end;return n
 end
 door_graph_system=setmetatable({_smart_object_id_to_extension={}}, {__index=NativeGraphSystem})
 local previous=Managers.state.extension.system
 Managers.state.extension.system=function(self,name)
  if name=="nav_graph_system" then return door_graph_system end
  return previous(self,name)
 end
 GwNavGraph={add_to_database=function(graph) graph.in_database=true end,
  remove_from_database=function(graph) graph.in_database=false end}
 door_open_calls=0
end

function make_door(id,state,open_type,enabled)
 local unit={extensions={}}
 local handle={}
 local graph=setmetatable({_unit=unit,_nav_graphs={handle},_nav_graph_added={},
  _smart_object_id_to_nav_graph={[id]=handle}}, {__index=NativeGraph})
 local door=setmetatable({_unit=unit,_type="two_states",_current_state=state or "closed",_open_type=open_type or "none",
  _entrance_nav_blocked=state~="open",_self_closing_time=0}, {__index=NativeDoor})
 -- Engine animation/network side effects of native open() finish immediately.
 door._free_companions=function() end
 door._set_server_state=function(self,new_state)
  door_open_calls=door_open_calls+1;self._current_state=new_state;self._entrance_nav_blocked=new_state=="closed"
 end
 unit.extensions.door_system=door;unit.extensions.nav_graph_system=graph;ALIVE[unit]=true
 door_graph_system:register_smart_object_id_to_extension(id,graph)
 local component=setmetatable({is_server=true,_nav_graph_extension=graph}, {__index=NativeGraphComponent})
 if enabled~=false then component:flow_nav_enable() end
 return door,component,unit
end

function door_context(t) now=t;return Placement.context(2,1,t) end
function path_door(id) placement_plan=function() return {graphs={1,2,id,7}} end end
function native_door_run(door)
 local unit={extensions={animation_system={anim_event=function() end}}}
 local scratch={door_unit_extension=door,rotation_done_time=0}
 local board={behavior={}}
 return NativeDoorAction.run({},unit,{},board,scratch,{},.1,1)
end

-- can_open is not a player-button permission query. The native AI checks the
-- same door state without an interactor and can directly open an enabled door.
door_setup()
local door,component,unit=make_door(9001)
local panel=setmetatable({_state="inactive"}, {__index=NativePanel})
assert(not panel:is_active() and door:can_open())
assert(native_door_run(door)=="done" and door_open_calls==1 and not door:nav_blocked())
door._current_state="closed";door._entrance_nav_blocked=true;door._open_type="close_only"
assert(not door:can_open() and native_door_run(door)=="running" and door_open_calls==1)
print("Actual native door behavior: inactive player panel does not itself prevent AI opening; closed non-openable door leaves the AI waiting: PASS")

-- A native successful route is authoritative even when an independently
-- inspected door looks blocked. Placement must never query door metadata.
local function forbid_door_queries()
 GwNavAStar.nav_graphs=function() error("extra transition inspection") end
 Managers.state.nav_mesh.nav_tag_layer_id=function() error("extra layer lookup") end
 local system=Managers.state.extension.system
 Managers.state.extension.system=function(self,name)
  assert(name~="nav_graph_system","extra door lookup")
  return system(self,name)
 end
end
for _,mode in ipairs({"blocked","disabled","dead","missing_door","missing_graph","unregistered","unknown_layer","malformed","unknown_state"}) do
 door_setup();door,component,unit=make_door(9001);path_door(9001)
 if mode=="blocked" then door._open_type="close_only"
 elseif mode=="disabled" then component:flow_nav_disable()
 elseif mode=="dead" then ALIVE[unit]=nil
 elseif mode=="missing_door" then unit.extensions.door_system=nil
 elseif mode=="missing_graph" then unit.extensions.nav_graph_system=nil
 elseif mode=="unregistered" then door_graph_system._smart_object_id_to_extension[9001]=nil
 elseif mode=="unknown_layer" then placement_layer_names[7]=nil
 elseif mode=="malformed" then placement_plan=function() return {graphs={1,2,9001}} end
 else door._entrance_nav_blocked=nil end
 forbid_door_queries()
 local anchor=Placement.anchor(door_context(0));assert(anchor,mode)
 assert(Placement.valid(door_context(0),anchor) and door_open_calls==0 and door._current_state=="closed",mode)
 Placement.finish();assert(#lines==0)
end
print("Complete native paths pass without extra door/graph/state/metadata inspection; no door interaction or diagnostic output: PASS")

for layer=8,14 do
 door_setup();placement_plan=function() return {graphs={1,2,9001,layer}} end
 forbid_door_queries();assert(Placement.anchor(door_context(0)),placement_layer_names[layer]);Placement.finish()
end
door_setup();door=make_door(9001,"closed","close_only")
placement_plan=function() return {graphs={1,2,9100,8,2,3,9101,9,3,4,9102,10,4,5,9103,11,5,6,9104,12,6,7,9001,7},count=7} end
forbid_door_queries()
local breeds={};for i=1,21 do breeds[i]="chaos_ogryn_executor" end
local manager={_nav_world=pm._nav_world,_pacing_type="default"}
local job=B.queue_native_patrol(manager,{breed_list={test={challenge_templates={breeds}}}},2,{groups={}})
for step=0,60 do now=step*.25;B.update_patrol_spawns(manager,now,2,1);if job.completed then break end end
assert(job.completed and #all_created==21 and #placement_engine.starts==1 and door_open_calls==0)
assert(not gs._locked_group_ids[job.group_id] and #lines==0)
Placement.finish()
print("All terrain links remain native; mixed route including a closed door creates 21 crushers via native groups using one shared path, without touching the door: PASS")

door_setup();door=make_door(9001);path_door(9001);forbid_door_queries()
local anchor=Placement.anchor(door_context(0));assert(anchor)
door._open_type="close_only"
assert(Placement.valid(door_context(0),anchor))
placement_live_valid=false;assert(not Placement.valid(door_context(0),anchor))
door_setup();placement_plan=function() return {found=false,graphs={1,2,9001,7}} end;forbid_door_queries()
assert(not Placement.anchor(door_context(0)))
door_setup();door=make_door(9001);placement_plan=function() return {done=false,graphs={1,2,9001,7}} end;forbid_door_queries()
assert(not Placement.anchor(door_context(0)))
door._open_type="close_only";placement_engine.handles[1].done=true
assert(Placement.anchor(door_context(.25)) and #placement_engine.starts==1)
print("Async completion and cached route reuse follow native path validity; failed or invalidated native paths still refuse spawning: PASS")

for _,invalidate in ipairs({false,true}) do
 door_setup();door=make_door(9001);path_door(9001);forbid_door_queries();pm.allowed=false
 roaming("renegade_executor");run(0,35);assert(#deleted==1)
 pm.allowed=true;now=40;B.update_straggler_recycling(pm,now);assert(ms._spawn_queue_size==1)
 door._open_type="close_only";placement_live_valid=not invalidate;ms:_update_spawn_queue()
 assert(ms._spawn_queue_size==0 and #all_created==(invalidate and 1 or 2) and door_open_calls==0)
 finish_recovery(invalidate and 1 or 0);Placement.finish()
 assert(placement_engine.created==1 and placement_engine.destroyed==1 and placement_engine.live_destroyed==1)
end
print("Actual native dequeue: door-state-only changes no longer cancel creation; native path invalidation still cancels and preserves one credit; all handles released: PASS")
""")
