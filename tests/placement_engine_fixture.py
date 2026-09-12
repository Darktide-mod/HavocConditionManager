"""Explicit engine boundary for AStar, live paths and local mesh projection.

Production placement and native spawn/queue methods still execute unmodified.
Scenarios may return delayed, missing, partial, dynamic or transition paths.
"""

def install(lua):
    lua.execute("""
function setup_placement_engine()
 if B.spawn_placement then B.spawn_placement.finish() end
 placement_engine={starts={},created=0,destroyed=0,live_created=0,live_destroyed=0,
  polls=0,checks=0,rays=0,projections=0,handles={}}
 placement_traverse={};placement_plan=nil;placement_ray_handler=nil;placement_floor=nil;placement_live_valid=true
 placement_layer_names={[7]="doors",[8]="ledges",[9]="ledges_with_fence",[10]="cover_ledges",
  [11]="cover_vaults",[12]="jumps",[13]="teleporters",[14]="monster_walls"}
 Managers.state.nav_mesh={nav_tag_layer_id=function(_,id) return placement_layer_names[id] end}
 function placement_ray(nav,from,to,traverse)
  placement_engine.rays=placement_engine.rays+1
  assert(traverse==placement_traverse)
  if placement_ray_handler then return placement_ray_handler(from,to) end
  return true
 end
 GwNavQueries.raycango=placement_ray
 local queries=require("scripts/utilities/nav_queries")
 queries.position_on_mesh_with_outside_position=function(nav,traverse,position,above,below,lateral)
  placement_engine.projections=placement_engine.projections+1
  assert(traverse==placement_traverse and above==1 and below==1 and lateral==1)
  if placement_floor then return placement_floor(position) end
  return vec(position[1],position[2],position[3])
 end
 GwNavAStar={
  create=function(nav)
   local a={nav=nav};placement_engine.created=placement_engine.created+1
   placement_engine.handles[#placement_engine.handles+1]=a;return a
  end,
  create_live_path=function() placement_engine.live_created=placement_engine.live_created+1;return {} end,
  start_with_propagation_box=function(a,nav,from,to,extent,traverse)
   assert(not a.dead and (not a.started or a.done),"concurrent reuse of an unfinished search")
   assert(nav==a.nav and extent==40 and traverse==placement_traverse)
   local plan=placement_plan and placement_plan(from,to) or {}
   a.started=true;a.done=plan.done~=false;a.found=plan.found~=false;a.graphs=plan.graphs
   a.count=plan.count or 2;a.goal=plan.goal or vec(to[1],to[2],to[3])
   placement_engine.starts[#placement_engine.starts+1]={from=Vector3Box(from),to=Vector3Box(to),t=now or 0}
  end,
  processing_finished=function(a) placement_engine.polls=placement_engine.polls+1;return a.done end,
  path_found=function(a) assert(a.done);return a.found end,
  nav_graphs=function(a) assert(a.done);return a.graphs end,
  node_count=function(a) assert(a.done);return a.count end,
  node_at_index=function(a,n) assert(a.done and n==a.count);return a.goal end,
  init_live_path=function(live,a) assert(a.done and a.found);live.ready=true end,
  is_valid=function(live,a)
   placement_engine.checks=placement_engine.checks+1
   assert(not live.dead and not a.dead and live.ready)
   return placement_live_valid
  end,
  destroy_live_path=function(live) assert(not live.dead);live.dead=true;placement_engine.live_destroyed=placement_engine.live_destroyed+1 end,
  destroy=function(a) assert(not a.dead);a.dead=true;placement_engine.destroyed=placement_engine.destroyed+1 end,
 }
end
""")
