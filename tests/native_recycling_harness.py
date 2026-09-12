"""Execute native perception scheduling, roamer creation, despawn and spawn queue.

Navigation projection, physics and engine entity creation are explicit boundaries.
This verifies behavior and query budgets, not in-game frame times.
"""
from native_harness import *

def method(path, owner, name):
    source=(game/path).read_text(encoding='utf-8-sig')
    start=source.index(owner+'.'+name+' = function')
    return source[start:source.index('\nend',start)+4]

L.execute('''
function class() return {} end
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.is_empty(t) return next(t)==nil end
function math.round_with_precision(v) return math.floor(v*100+.5)/100 end
NativeMinion={};NativeRoamer={};NativePerception={};NativeSystem={};NativePacing={};NativeObjective={};NativePatrol={}
local vec_mt={__index=function(v,k) if k=="z" then return v[3] end end,
 __add=function(a,b) return setmetatable({a[1]+b[1],a[2]+b[2],a[3]+b[3]},getmetatable(a)) end,
 __sub=function(a,b) return setmetatable({a[1]-b[1],a[2]-b[2],a[3]-b[3]},getmetatable(a)) end}
function vec(x,y,z) return setmetatable({x,y or 0,z or 0},vec_mt) end
Vector3={length=function(v) return math.sqrt(v[1]^2+v[2]^2+v[3]^2) end,
 normalize=function(v) return v end,distance_squared=function(a,b) local d=a-b;return d[1]^2+d[2]^2+d[3]^2 end}
Vector3.up=function() return vec(0,0,1) end
Vector3.to_elements=function(v) return v[1],v[2],v[3] end
Vector3.length_squared=function(v) return v[1]^2+v[2]^2+v[3]^2 end
EngineOptimized={point_on_mainpath=function(d) return vec(d) end}
Vector3.distance=function(a,b) return math.sqrt(Vector3.distance_squared(a,b)) end
function Vector3Box(v)
 local copy=vec(v[1],v[2],v[3])
 return {unbox=function() return vec(copy[1],copy[2],copy[3]) end,
  store=function(_,value) copy=vec(value[1],value[2],value[3]) end}
end
QuaternionBox=Vector3Box;Quaternion={identity=function() return vec(0) end}
GameParameters={};DEDICATED_SERVER=false;ALIVE={};HEALTH_ALIVE={};BLACKBOARDS={};POSITION_LOOKUP={}
ScriptUnit={extension=function(u,name) return u.extensions[name] end,has_extension=function(u,name) return u.extensions and u.extensions[name] end}
Blackboard={write_component=function(board,name) return board[name] end}
DialogueBreedSettings={};Vo={};NavQueries={position_on_mesh=function() return true end}
MinionPerception={line_of_sight_positions=function(unit,target)
 los_source,los_target=unit,target;return POSITION_LOOKUP[unit],POSITION_LOOKUP[target]
end}
PhysicsWorld={raycast=function(_,position)
 if position[1]>180 then spawn_los_queries=spawn_los_queries+1;return not spawn_visible end
 physics_queries=physics_queries+1;return not los_source.visible[los_target]
end}
GwNavSpawnPoints={get_count=function() return 40,1 end,
 get_group_from_position=function() return true,21,1 end,
 get_occluded_points=function(_,nav,group) native_point_groups=native_point_groups+1;return group==22 and hidden_position and {hidden_position} or {} end}
GwNavOccludedPointCollection={get_count=function(points) return #points end,get_position=function(points,nav,index) return points[index] end}
''')
L.globals().NativeEvent=lua_file(game/'scripts/managers/event/event_manager.lua')
for dependency in ('scripts/game_states/game/utilities/gameplay_init_time_slice','scripts/utilities/nav_queries'):
    cache[dependency]=tbl({})
L.globals().NativePoints=lua_file(game/'scripts/managers/main_path/utilities/spawn_point_queries.lua')
L.globals().Breeds=cache['scripts/settings/breed/breeds']
for owner,target,path,names,prefix in [
 ('MinionSpawnManager','NativeMinion','scripts/managers/minion/minion_spawn_manager.lua',
  ('init','request_param_table','spawn_minion','_initialize_inventory','_initialize_blackboard_components','unregister_unit','despawn_minion','queue_minion_to_spawn','_update_spawn_queue','total_allocated_num_enemies'),
  'local MINION_QUEUE_RING_BUFFER_SIZE=256;local TEMP_INIT_DATA={};'),
 ('RoamerPacing','NativeRoamer','scripts/managers/pacing/roamer_pacing/roamer_pacing.lua',
  ('_try_activate_roamer','_spawn_roamer','_deactivate_roamer'),
  'local NAV_ABOVE,NAV_BELOW=.1,.1;local function _roamer_is_passive(u) return HEALTH_ALIVE[u] and BLACKBOARDS[u].perception.aggro_state=="passive" end;'),
 ('MinionPerceptionExtension','NativePerception','scripts/extension_systems/perception/minion_perception_extension.lua',
  ('update','has_line_of_sight','immediate_line_of_sight_check','alert','aggro','is_perception_disabled'),
  'local aggro_states={passive="passive",alerted="alerted",aggroed="aggroed"};'),
 ('MissionObjectiveTargetExtension','NativeObjective','scripts/extension_systems/mission_objective_target/mission_objective_target_extension.lua',
  ('init','objective_name','_setup'),''),
 ('BtPatrolAction','NativePatrol','scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua',
  ('_update_patrolling',),''),
 ('PerceptionSystem','NativeSystem','scripts/extension_systems/perception/perception_system.lua',('update',),'local UPDATE_ALL_UNITS_TIME=1;'),
 ('PacingManager','NativePacing','scripts/managers/pacing/pacing_manager.lua',('remove_aggroed_minion',),''),
]:
    for name in names: L.execute('local '+owner+'='+target+';'+prefix+method(path,owner,name))
L.execute('math.random_seed=function(seed) return seed+1 end')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks')
from placement_engine_fixture import install
install(L)
L.execute('''
local function hook(path,name)
 local target=require(path)
 for _,h in ipairs(hooks) do if h.target==target and h.name==name then return h.fn end end
 error(name)
end
local observe=hook("scripts/extension_systems/perception/minion_perception_extension","update")
local activated=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","_try_activate_roamer")
deactivated=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","_deactivate_roamer")
local drain=hook("scripts/managers/minion/minion_spawn_manager","_update_spawn_queue")
local queries=require("scripts/managers/main_path/utilities/spawn_point_queries")
lines={};function B:info(message,...) lines[#lines+1]=string.format(message,...) end
-- Test-only inspection of the real pending queue. Production needs no
-- reporting counters or public diagnostic interface to verify conservation.
function recovery_state()
 for i=1,20 do
  local name,value=debug.getupvalue(B.update_straggler_recycling,i)
  if not name then break end
  if name=="state" then return value end
 end
end
function recovery_pending()
 local s=recovery_state()
 if not s then return 0 end
 local pending=0
 assert(#s.credits<=32 and s.ready_size<=64)
 for _,credit in ipairs(s.credits) do pending=pending+#credit.breeds-(credit.index or 1)+1 end
 assert(pending==s.credit_units and pending<=256,"pending allowance accounting")
 return pending
end
function finish_recovery(expected)
 assert(recovery_pending()==expected,"unexpected remaining allowance")
 B.finish_straggler_recycling()
 assert(not recovery_state() and #lines==0,"diagnostic output or retained state")
end
function setup()
 B.finish_straggler_recycling();B.finish_spawn_tracking();host=true;lines={}
 B.values.native_configuration_v3={};Managers.state.game_session={};E.reset()
 now=0;physics_queries=0;spawn_los_queries=0;spawn_visible=false;position_queries=0;projection_queries=0;native_ticks=0;native_point_groups=0
 ALIVE={};HEALTH_ALIVE={};BLACKBOARDS={};POSITION_LOOKUP={};deleted={};all_created={}
 players={{bot=false},{bot=true},{bot=true},{bot=true}}
 for i,u in ipairs(players) do HEALTH_ALIVE[u]=true;ALIVE[u]=true;POSITION_LOOKUP[u]=vec(200+i) end
 enemy_side={side_id=2,enemy_player_units=players,ai_target_units={},ai_ground_target_units={},valid_enemy_player_units_positions={}}
 for i,u in ipairs(players) do enemy_side.valid_enemy_player_units_positions[i]=POSITION_LOOKUP[u] end
 sides={side_by_unit={},get_side=function() return enemy_side end,remove_aggroed_minion=function() end,
  get_objective_group_id_from_unit=function() return 0 end,register_objective_unit=function() end}
 Managers.state.extension={system=function() return sides end}
 Managers.time={time=function() return now end}
 Managers.event=setmetatable({}, {__index=NativeEvent});Managers.event:init();B.start_spawn_tracking()
 Managers.state.game_mode={game_mode=function() return {extension=function() return nil end,name=function() return "test" end} end}
 Managers.state.mutator={mutator=function() return nil end}
 main={is_main_path_ready=function() return main.ready end,ready=true,
  travel_distance_from_position=function(_,pos) projection_queries=projection_queries+1;return pos[1] end,
  ahead_unit=function() return players[1],POSITION_LOOKUP[players[1]][1] end,nav_spawn_points=function() return {} end,spawn_point_cost_table=function() return {} end}
 Managers.state.main_path=main
 pm=setmetatable({_aggroed_minions={},_saved_challenge_ratings={},_minions_listening_for_player_deaths={},
  _num_aggroed_minions=0,_total_challenge_rating=0,_side_system=sides,_target_side_id=1,_nav_world={},allowed=false}, {__index=NativePacing})
 function pm:_get_challenge_rating(u) return self._saved_challenge_ratings[u] end
 function pm:spawn_type_enabled(kind) assert(kind=="roamers");return self.allowed end
 function pm:get_in_safe_zone() return self.safe end
 function pm:roamer_traverse_logic() return placement_traverse end
 Managers.state.horde={_physics_world={}}
 Managers.state.pacing=pm
 ms=setmetatable({replacement_breed=function() end}, {__index=NativeMinion});ms:init(12,{},nil);Managers.state.minion_spawn=ms
 ms._update_spawn_queue=function(self) return drain(NativeMinion._update_spawn_queue,self) end
 sensor=setmetatable({_update_units={},_num_update_units=0,_prioritized_update_units={},update_extension=function() end}, {__index=NativeSystem})
 Managers.state.unit_spawner={mark_for_deletion=function(_,u) deleted[#deleted+1]=u end,
  spawn_network_unit=function(_,a,b,position,rotation,c,data)
   local unit={extensions={},visible={},keywords={}};all_created[#all_created+1]=unit
   HEALTH_ALIVE[unit]=true;ALIVE[unit]=true;POSITION_LOOKUP[unit]=position;sides.side_by_unit[unit]=enemy_side
   BLACKBOARDS[unit]={spawn={},group_data={},perception={aggro_state=data.optional_aggro_state or "passive"}}
   local ext=setmetatable({_unit=unit,_breed=data.breed,_side_system=sides,_perception_system=sensor,_delayed_alerts={},_line_of_sight_lookup={},
    _line_of_sight_data={{from_offsets={}}},_perception_component=BLACKBOARDS[unit].perception}, {__index=NativePerception})
   function ext:_update_target_selection() return self.selected end
   function ext:_set_target_unit(target) self._perception_component.target_unit=target;return true end
   function ext:_update_aggro_state() end
   function ext:_update_priority_blackboard_status() end
   function ext:update(u,dt,t) native_ticks=native_ticks+1;NativePerception.update(self,u,dt,t);observe(self,u,dt,t) end
   unit.extensions.perception_system=ext
   local initialized_breed=data.breed
   unit.extensions.unit_data_system={breed=function() return initialized_breed end}
   unit.extensions.navigation_system={is_following_path=function() return unit.following end,is_using_smart_object=function() return unit.traversing end}
   unit.extensions.health_system={current_health_percent=function() return unit.health or 1 end,last_damaging_unit=function() return unit.damaged_by end,is_invulnerable=function() return unit.invulnerable end}
   unit.extensions.buff_system={has_keyword=function(_,k) return unit.keywords[k] end}
   unit.extensions.smart_tag_system={tag_id=function() return unit.tagged end}
   local objective=setmetatable({}, {__index=NativeObjective})
   objective:init({is_server=true},unit,{})
   objective:_setup()
   assert(objective:objective_name()=="default" and not objective._registered_objective)
   unit.extensions.mission_objective_target_system=objective
   sensor._update_units[unit]=ext;sensor._num_update_units=sensor._num_update_units+1
   return unit
  end}
 rp=setmetatable({_roamer_lookup={},_patrol_data={patrols={},active_patrols={}},_roamers={},_num_roamers=0,
  _roamer_update_index=1,_handle_group_ambience_sfx=function() end}, {__index=NativeRoamer})
 function queries.get_occluded_positions(nav,points,origin,targets,range,groups,min,max,offset,forward)
  position_queries=position_queries+1;assert(groups==40 and range==4 and
   (min==35 and max==120 and forward or min==20 and max==60 and not forward))
  local before=native_point_groups
  local result,count=NativePoints.get_occluded_positions(nav,points,origin,targets,range,groups,min,max,offset,forward)
  assert(native_point_groups-before<=5,"native forward position search exceeded group budget")
  return result,count
 end
 GwNavQueries={flood_fill_from_position=function(_,pos,a,b,n,output)
  for i=1,n do output[i]=vec(pos[1]+i*.5) end;return n
 end}
 hidden_position=vec(250)
 setup_placement_engine()
end
function roaming(breed)
 local r={breed_name=breed or "chaos_poxwalker",position=Vector3Box(vec(0)),rotation=Vector3Box(vec(0))}
 rp._roamers[#rp._roamers+1]=r;rp._num_roamers=rp._num_roamers+1
 assert(rp:_try_activate_roamer(r,2));activated(rp,r,2)
 local u=r.spawned_unit;BLACKBOARDS[u].perception.aggro_state="aggroed";pm._aggroed_minions[u]=true;pm._saved_challenge_ratings[u]=2
 pm._total_challenge_rating=pm._total_challenge_rating+2;pm._num_aggroed_minions=pm._num_aggroed_minions+1
 return u,r,u.extensions.perception_system
end
function tick(t)
 now=t
 for _,u in ipairs(all_created) do
  if u.test_motion then POSITION_LOOKUP[u]=u.test_motion(t) end
  if u.ongoing_damage then hook("scripts/extension_systems/health/health_extension","add_damage")({_unit=u},1) end
 end
 sensor:update(nil,1,t);B.update_straggler_recycling(pm,t)
end
function run(a,b) for t=a,b do tick(t) end end
''')

# Patrol tests retain the actual group lifecycle and both native patrol spawners.
L.execute('NativeGroup={};NativeMonster={};NativeHorde={};NativeTrickle={name="trickle_horde",occluded_spawn_range=3};MinionPatrols={}')
for owner,target,path,names,prefix in [
 ('GroupSystem','NativeGroup','scripts/extension_systems/group/group_system.lua',
  ('_create_group','generate_group_id','group_from_id','_add_member_to_group','_remove_member_from_group','_remove_group','lock_group_id','unlock_group_id'),
  'local DEFAULT_MIN_MINIONS=5;'),
 ('MonsterPacing','NativeMonster','scripts/managers/pacing/monster_pacing/monster_pacing.lua',('_spawn_boss_patrol',),
  'local pacing_types={default="default",timer_based="timer_based"};local perception_aggro_states={passive="passive"};'),
 ('HordeManager','NativeHorde','scripts/managers/horde/horde_manager.lua',('horde',),
  'local HordeTemplates={trickle_horde=NativeTrickle};'),
 ('MinionPatrols','MinionPatrols','scripts/utilities/minion_patrols.lua',('get_follow_index',),''),
]:
    for name in names: L.execute('local '+owner+'='+target+';'+prefix+method(path,owner,name))
L.globals().NativeGroupExtension=lua_file(game/'scripts/extension_systems/group/minion_group_extension.lua')
trickle_path='scripts/managers/horde/templates/trickle_horde_template.lua'
trickle_source=(game/trickle_path).read_text(encoding='utf-8-sig')
compose=trickle_source[trickle_source.index('local function _compose_spawn_list'):trickle_source.index('local MIN_DISTANCE_FROM_PLAYERS')]
L.execute('''local horde_template=NativeTrickle;local TEMP_BREED_NAMES={};
local aggro_states={passive="passive",aggroed="aggroed"};local PATROL_CHALLENGE_RAITNG_THRESHOLD=8;
local function _try_find_horde_position() return vec(0),vec(1),players[1] end;
'''+compose+method(trickle_path,'horde_template','execute'))
L.execute('''
function table.index_of(t,v) for i,x in ipairs(t) do if x==v then return i end end end
function table.swap_delete(t,i) t[i]=t[#t];t[#t]=nil end
function table.shuffle() end
function table.clear_array(t) table.clear(t) end
setmetatable(Vector3,{__call=function(_,x,y,z) return vec(x,y,z) end})
Quaternion.look=function() return vec(0) end
local function hook(path,name)
 for _,h in ipairs(hooks) do if h.target==require(path) and h.name==name then return h.fn end end
 error(name)
end
local boss_hook=hook("scripts/managers/pacing/monster_pacing/monster_pacing","_spawn_boss_patrol")
local horde_hook=hook("scripts/managers/horde/horde_manager","horde")
local activation_hook=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","_try_activate_roamer")
function patrol_setup()
 setup()
 gs=setmetatable({_groups={},_num_groups=0,_current_group_id=0,_locked_group_ids={},_unit_to_extension_map={}}, {__index=NativeGroup})
 Managers.state.extension.system=function(_,name) return name=="group_system" and gs or sides end
 local engine=Managers.state.unit_spawner
 local create,remove=engine.spawn_network_unit,engine.mark_for_deletion
 function engine:spawn_network_unit(a,b,pos,rotation,c,data)
  local u=create(self,a,b,pos,rotation,c,data)
  BLACKBOARDS[u].patrol={walk_position=Vector3Box(vec(0))}
  u.health_modifier=data.optional_health_modifier
  if data.optional_group_id then
   local ge=setmetatable({}, {__index=NativeGroupExtension})
   ge:init({},u,{group_id=data.optional_group_id})
   gs._unit_to_extension_map[u]=ge;u.extensions.group_system=ge
   gs:_add_member_to_group(u,data.optional_group_id);ge:extensions_ready({},u)
  end
  return u
 end
 function engine:mark_for_deletion(u)
  remove(self,u)
  local ge=u.extensions.group_system
  if ge and ge:group_id() then gs:_remove_member_from_group(u,ge:group_id()) end
 end
 function pm:spawn_type_enabled(kind) assert(kind=="monsters" or kind=="trickle_hordes" or kind=="roamers");return self.allowed end
 function pm:current_faction() return "test" end
 function pm:total_challenge_rating() return 0 end
 function pm:waiting_for_ramp_clear() return false end
 function pm:heat_trickle_should_patrol() return true end
 function pm:exp_random_position_away_from_players() end
 main.ahead_unit=function() return players[1],201,POSITION_LOOKUP[players[1]] end
 MainPathQueries={position_from_distance=function(d) return vec(d) end}
 Managers.state.difficulty={get_table_entry_by_challenge=function(_,t) return t end}
 GwNavQueries={flood_fill_from_position=function(_,pos,a,b,n,output)
  for i=1,n do output[i]=queue_spawning and vec(pos[1]+i*.5) or vec(i-1,0,0) end;return n
 end}
 GwNavQueries.raycango=placement_ray
 local points=require("scripts/managers/main_path/utilities/spawn_point_queries")
 function points.get_occluded_positions(...)
  position_queries=position_queries+1;local before=native_point_groups
  local a,b=NativePoints.get_occluded_positions(...)
  assert(native_point_groups-before<=5);return a,b
 end
 GwNavSpawnPoints.get_occluded_points=function(_,nav,group)
  native_point_groups=native_point_groups+1
  if group~=22 then return {} end
  local points={};for i=1,(available_points or 64) do points[i]=vec(240+i,0,0) end;return points
 end
 available_points=64
end
function boss_patrol(n,options)
 local list={};for i=1,n do list[i]=i%2==0 and "renegade_executor" or "chaos_poxwalker" end
 local boss={breed_list={test={challenge_templates={list}}},spawn_point_travel_distance=0,spawn_position=Vector3Box(vec(0))}
 local pacing={_pacing_type="default",_nav_world={}}
 for k,v in pairs(options or {}) do pacing[k]=v end
 local pending=boss_hook(NativeMonster._spawn_boss_patrol,pacing,boss,201,2)
 if pacing._pacing_type=="default" then
  assert(pending and #all_created==ms._num_spawned_minions)
  local allowed=pm.allowed;pm.allowed=true;queue_spawning=true
  for frame=0,2000 do
   B.update_patrol_spawns(pacing,frame*.05,2,1)
   if pending.completed then break end
  end
  assert(pending.completed)
  pm.allowed=allowed;queue_spawning=nil
  -- Normalize the subsequent rear-qualification fixture after deployment.
  for i,u in ipairs(pending.units) do POSITION_LOOKUP[u]=vec(i-1) end
 end
 local group=gs._groups[#gs._groups]
 for _,u in ipairs(group.members) do u.following=true end
 return group
end
function trickle_patrol(options)
 local manager={_hordes={trickle={}},_nav_world={},_physics_world={}}
 local composition={breeds={{name="renegade_executor",amount={6,6}}}}
 local ok,position,target,id=horde_hook(NativeHorde.horde,manager,"trickle","trickle_horde",2,1,composition,
  nil,nil,nil,nil,1.5,nil,nil,nil,options)
 assert(ok and id and position and target)
 local group=gs:group_from_id(id)
 for _,u in ipairs(group.members) do u.following=true end
 return group
end
''')
