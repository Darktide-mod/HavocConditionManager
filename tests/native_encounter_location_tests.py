"""Reproduce shared-section starvation and run the extended native encounters."""
from native_harness import *


def extract(name):
    source=(GAME/'scripts/managers/pacing/monster_pacing/monster_pacing.lua').read_text(encoding='utf-8-sig')
    start=source.index('MonsterPacing.'+name+' = function')
    return source[start:source.index('\nend',start)+4]


L.execute('''
NativeMonster={}; injections={};native_warnings={};info_lines={}
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function table.clear_array(t,n) for i=1,n do t[i]=nil end end
function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
function table.swap_delete(t,i) t[i]=t[#t];t[#t]=nil end
Log={info=function() end,warning=function(tag,message,...) native_warnings[#native_warnings+1]={tag=tag,message=string.format(message,...)} end}
function B:info(message,...) info_lines[#info_lines+1]=string.format(message,...) end
''')
prefix='''local MonsterPacing=NativeMonster
local MonsterSettings=require("scripts/settings/monster/monster_settings")
local MonsterInjectionTemplates=injections
local TEMP_SECTIONS_MONSTERS,TEMP_SECTIONS_WITCHES,NUM_SECTIONS={},{},{}
local function _sort_spawners(a,b) return a.spawn_travel_distance<b.spawn_travel_distance end
local pacing_types={default="default",timer_based="timer_based"}
local perception_aggro_states={passive="passive",aggroed="aggroed"}
local MainPathQueries={position_from_distance=function(d) return {d,0,0} end}
local Blackboard={write_component=function(b,k) return b[k] end}
local MinionPatrols={get_follow_index=function(i) return 1 end}
'''
L.execute(prefix+'\n'.join(extract(n) for n in ('_generate_spawns','update','_spawn_monster','_spawn_boss_patrol','_setup_timer_based_monster_pacing','_update_allowance')))
original_loader=L.globals().load_mod_file
def capture_reserve(path):
    module=load_mod(path)
    if path.endswith('/encounter_reserve'): L.globals().reserve_module=module
    return module
L.globals().load_mod_file=capture_reserve
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks')
from placement_engine_fixture import install
install(L)
# Full path admission is exercised separately with asynchronous engine results.
L.globals().load_mod_file=original_loader
query_source=(GAME/'scripts/managers/main_path/utilities/spawn_point_queries.lua').read_text(encoding='utf-8-sig')
query_start=query_source.index('SpawnPointQueries.get_random_occluded_position = function')
L.execute('local SpawnPointQueries=require("scripts/managers/main_path/utilities/spawn_point_queries");'+query_source[query_start:query_source.index('\nend',query_start)+4])
# The campaign safety flag is exercised through the actual native methods.
for path,owner,target,names in (
    ('scripts/managers/pacing/pacing_manager.lua','PacingManager','NativeSafePacing',('set_in_safe_zone','get_in_safe_zone')),
    ('scripts/managers/game_mode/game_modes/game_mode_coop_complete_objective.lua','GameModeCoopCompleteObjective','NativeSafeMode',('_restrict_spawning',)),
):
    L.execute(target+'={}')
    source=(GAME/path).read_text(encoding='utf-8-sig')
    for name in names:
        start=source.index(owner+'.'+name+' = function')
        L.execute('local '+owner+'='+target+';'+source[start:source.index('\nend',start)+4])
L.execute('''
local vmt={__index=function(v,k) if k=="z" then return v[3] end end,
 __add=function(a,b) return setmetatable({a[1]+b[1],a[2]+b[2],a[3]+b[3]},getmetatable(a)) end,
 __sub=function(a,b) return setmetatable({a[1]-b[1],a[2]-b[2],a[3]-b[3]},getmetatable(a)) end}
function vec(x,y,z) return setmetatable({x,y or 0,z or 0},vmt) end
Vector3={up=function() return vec(0,0,1) end,length_squared=function(v) return v[1]^2+v[2]^2+v[3]^2 end,
 normalize=function(v) return v end,distance_squared=function(a,b) return (a[1]-b[1])^2+(a[2]-b[2])^2+(a[3]-b[3])^2 end}
setmetatable(Vector3,{__call=function(_,x,y,z) return vec(x,y,z) end})
EngineOptimized={point_on_mainpath=function(d) return vec(d) end}
PhysicsWorld={raycast=function() return true end}
GwNavSpawnPoints={get_count=function() return 40 end}
Managers.state.horde={_physics_world={}}
local class=require("scripts/managers/pacing/monster_pacing/monster_pacing")
local generate,update_hook,destroy_hook,post_init_hook
for _,h in ipairs(hooks) do
 if h.target==class and h.name=="_generate_spawns" then generate=h.fn end
 if h.target==class and h.name=="update" then update_hook=h.fn end
 if h.target==class and h.name=="destroy" then destroy_hook=h.fn end
 if h.target==class and h.name=="on_gameplay_post_init" then post_init_hook=h.fn end
 if h.target==Log and h.name=="warning" then local original=Log.warning;Log.warning=function(...) return h.fn(original,...) end end
end
assert(generate)
local original_random=math.random
math.random=function(a,b) if b then return a end;if a then return 1 end;return .5 end
local base=require("scripts/managers/pacing/pacing_templates").default.monster_pacing_template.challenge_templates[5]
local function configure(monsters,patrols)
 B.values.native_configuration_v3={monster_encounters=monsters,patrols=patrols}
 Managers.state.game_session={};E.reset();host=true;table.clear(warnings);table.clear(native_warnings);table.clear(info_lines)
end
local havoc_extra=0
local position=0
Managers.state.main_path={is_main_path_available=function() return true end,ahead_unit=function() return "player",position end,behind_unit=function() return "player",0 end}
Managers.state.difficulty={get_table_entry_by_challenge=function(_,t) return t[5] end,get_resistance=function() return 5 end}
Managers.state.game_mode={game_mode=function() return {extension=function() return {get_modifier_value=function() return havoc_extra end} end} end}
local function make_manager(points_per_section)
 local sections={monsters={},witches={},captains={}}
 for section=1,3 do
  for _,kind in ipairs({"monsters","witches","captains"}) do
   sections[kind][section]={}
   for i=1,points_per_section do
    local d=(section-1)*600+i*40
    local vector={d,0,0}
    sections[kind][section][i]={spawn_travel_distance=d,spawn_point_travel_distance=d+40,position={unbox=function() return vector end}}
   end
  end
 end
 local template=S.copy(base)
 template.num_spawns={monsters={8,8},witches=0,captains=0}
 template.boss_patrols.num_boss_patrols_range={6,6}
 return setmetatable({_template=template,_pacing_type="default",_health_modifier=1,_aggroed_monster_units={},
  _main_path_sound_events={},_spawn_type_point_sections=sections,_num_spawn_type_sections={monsters=3,witches=3,captains=3},
  _get_captain_faction=function(_,m) return m end}, {__index=NativeMonster})
end
local function count_monsters(self)
 local n=0;for _,m in ipairs(self._monsters) do if m.spawn_type=="monsters" then n=n+1 end end;return n
end
configure(5,6)
local old=make_manager(15)
assert(NativeMonster._generate_spawns(old,old._template))
assert(count_monsters(old)==3 and #old._boss_patrols==0,"native shared sections must reproduce patrol starvation")
local updated=make_manager(15)
assert(generate(NativeMonster._generate_spawns,updated,updated._template))
assert(count_monsters(updated)==8 and #updated._boss_patrols==6)
assert(updated._template.num_spawns.monsters[1]==8 and updated._template.boss_patrols.num_boss_patrols_range[1]==6)
assert(updated._num_monsters_override==nil and updated._num_boss_patrol_override==nil)
local authored={}
for _,section in ipairs(updated._spawn_type_point_sections.monsters) do
 for _,point in ipairs(section) do authored[point.position]=true end
end
local distances={};local point_distances={}
for _,m in ipairs(updated._monsters) do
 assert(authored[m.position],"only original boxed map positions may be used")
 assert(not point_distances[m.travel_distance]);point_distances[m.travel_distance]=true
 distances[#distances+1]=m.travel_distance
end
for _,patrol in ipairs(updated._boss_patrols) do
 assert(patrol.breed_list==updated._template.boss_patrols.breed_lists)
 local d=patrol.spawn_point_travel_distance-40
 assert(not point_distances[d]);point_distances[d]=true;distances[#distances+1]=patrol.travel_distance
end
table.sort(distances)
for i=2,#distances do assert(distances[i]-distances[i-1]>=10) end
-- Scarce real positions cannot be duplicated to pretend quotas were achieved.
local sparse=make_manager(1)
assert(generate(NativeMonster._generate_spawns,sparse,sparse._template))
assert(count_monsters(sparse)+#sparse._boss_patrols<=3 and #warnings==0)
assert(count_monsters(sparse)+sparse._hcm_encounter_reserve.monsters==8)
assert(#sparse._boss_patrols+sparse._hcm_encounter_reserve.patrols==6)
assert(#info_lines==0)
-- One extra position is offered to the starved patrol quota before monsters.
local few=make_manager(1)
local duplicate_position={100,0,0}
few._spawn_type_point_sections.monsters[1][2]={spawn_travel_distance=100,spawn_point_travel_distance=140,position={unbox=function() return duplicate_position end}}
assert(generate(NativeMonster._generate_spawns,few,few._template))
assert(#few._boss_patrols>=1)
-- No mutation of the global template or native overrides, including errors.
local overrides=make_manager(15);overrides._num_monsters_override=9;overrides._num_boss_patrol_override=7
assert(generate(NativeMonster._generate_spawns,overrides,overrides._template))
assert(count_monsters(overrides)==9 and #overrides._boss_patrols==7)
assert(overrides._num_monsters_override==9 and overrides._num_boss_patrol_override==7)
local ok=pcall(generate,function() error("expected failure") end,overrides,overrides._template)
assert(not ok and overrides._num_monsters_override==9 and overrides._num_boss_patrol_override==7)
assert(not B.defer_native_encounter_warning(function() end,"MonsterPacing","Requested %s spawns for type %s but only had %s sections. Clamped.",9,"monsters",3))
-- Native objective injections stay single records with all overrides/sounds.
injections.required={difficulties={true,true,true,true,true},should_inject=function() return true end,
 breed_names={"renegade_captain"},add_overrides=function(m) m.objective="required_objective";m.set_enraged=true end,
 sound_data={event="required_sound",distance=5}}
local injected=make_manager(15)
assert(generate(NativeMonster._generate_spawns,injected,injected._template))
local objectives=0
for _,m in ipairs(injected._monsters) do if m.objective then objectives=objectives+1;assert(m.set_enraged and m.breed_name=="renegade_captain") end end
assert(objectives==1 and #injected._main_path_sound_events==1)
table.clear(injections)
-- Native Havoc additions apply once; the provisional section clamp is no
-- longer presented as a final failure when unused positions fulfill it.
configure(5,6);havoc_extra=4
local extra=make_manager(15)
assert(generate(NativeMonster._generate_spawns,extra,extra._template))
assert(count_monsters(extra)==12 and #extra._boss_patrols==6)
assert(#native_warnings==0 and #warnings==0 and #info_lines==0)
havoc_extra=0
local zero=make_manager(15);zero._num_monsters_override=0;zero._num_boss_patrol_override=0
assert(generate(NativeMonster._generate_spawns,zero,zero._template))
assert(count_monsters(zero)==0 and #zero._boss_patrols==0)
-- Heat-based missions use the native allowance and timer consumers.
local heat_base=require("scripts/managers/pacing/monster_pacing/templates/expedition_monster_pacing_template").challenge_templates[5]
local heat_template=S.apply(heat_base,"monsters",S.coarse_config({monster_encounters=5,patrols=6}),nil,A.breeds,A.by_table)
assert(heat_base.max_allowed_by_heat[3].monsters==1 and heat_base.max_allowed_by_heat[3].boss_patrols==1)
assert(heat_template.max_allowed_by_heat[3].monsters==5 and heat_template.max_allowed_by_heat[3].boss_patrols==6)
assert(heat_template.max_allowed_by_heat[1].boss_patrols==0)
local heat={_template=heat_template,_check_alive=function() end}
NativeMonster._setup_timer_based_monster_pacing(heat,0,0,2,1)
assert(math.abs(heat._next_monster_at_t-heat_base.monster_timer_range[1]/6)<.00001)
Managers.state.pacing={get_table_entry_by_heat_stage=function(_,t) return t[3] end}
assert(NativeMonster._update_allowance(heat,0,0,2,1) and heat._amount_allowed_by_type.total==11)
for i=1,5 do heat._currently_spawned_by_timer.monsters[i]={} end
for i=1,6 do heat._currently_spawned_by_timer.boss_patrols[i]={} end
assert(not NativeMonster._update_allowance(heat,0,0,2,1))
-- Local defaults and remote play retain the original planner, including RNG.
configure(1,1);local defaults=make_manager(15)
assert(generate(NativeMonster._generate_spawns,defaults,defaults._template) and count_monsters(defaults)==3 and #defaults._boss_patrols==0)
configure(5,6);host=false;local remote=make_manager(15)
assert(generate(NativeMonster._generate_spawns,remote,remote._template) and count_monsters(remote)==3 and #remote._boss_patrols==0);host=true

-- Consume the complete plan through the actual native update and spawn methods.
HEALTH_ALIVE={};BLACKBOARDS={};Quaternion={identity=function() return {} end}
local units,groups={},{}
local group_system={generate_group_id=function() local id=#groups+1;groups[id]={members={}};return id end,group_from_id=function(_,id) return groups[id] end,
 lock_group_id=function(_,id) groups[id].locked=true end,unlock_group_id=function(_,id) groups[id].locked=nil end}
Managers.state.extension={system=function(_,name) if name=="group_system" then return group_system end;return {trigger_wwise_event=function() end} end}
Managers.state.pacing={spawn_type_enabled=function() return true end,current_faction=function() return "renegade" end,pause_spawn_type=function() end,
 get_in_safe_zone=function(self) return self.safe end,_nav_world={}}
Managers.state.mutator={mutator=function() return false end}
Managers.event={trigger=function() end}
Managers.state.minion_spawn={_spawn_queue_size=0,total_allocated_num_enemies=function() return 0 end,
 request_param_table=function() return {} end,spawn_minion=function(_,breed,pos,rot,side,params)
 local u={breed=breed,params=params,position={pos[1],pos[2],pos[3]}};units[#units+1]=u;HEALTH_ALIVE[u]=true
 BLACKBOARDS[u]={patrol={walk_position={store=function(_,p) u.walk_position={p[1],p[2],p[3]} end}},
  perception={aggro_state=params.optional_aggro_state or "passive"}}
 if params.optional_group_id then local members=groups[params.optional_group_id].members;members[#members+1]=u end
 return u
end}
GwNavQueries={flood_fill_from_position=function(_,pos,above,below,n,output)
 for i=1,n do output[i]=vec(pos[1]+i) end;return n
end}
updated._main_path_sound_events={}
for d=0,2500,10 do position=d;updated:update(.1,d/10,2,1) end
for i=1,40 do updated:update(.1,251+i/10,2,1) end
assert(#updated._monsters==0 and #updated._boss_patrols==0)
assert(#updated._alive_monsters==8 and #groups==6)
local elite_members=0
local patrol_members=0
local breeds=require("scripts/settings/breed/breeds")
for _,group in ipairs(groups) do
 patrol_members=patrol_members+#group.members;assert(#group.members>0)
 for _,unit in ipairs(group.members) do if breeds[unit.breed].tags.elite then elite_members=elite_members+1 end end
end
assert(elite_members>0)
spawned_monsters=#updated._alive_monsters;spawned_patrols=#groups;spawned_patrol_members=patrol_members;spawned_elites=elite_members
for _,u in ipairs(units) do assert(u.params.optional_health_modifier==1 or u.params.optional_group_id) end

-- Only three static points: retain every remaining encounter as finite waves.
assert(update_hook and destroy_hook)
configure(5,6);units,groups={},{}
local deferred=make_manager(1)
assert(generate(NativeMonster._generate_spawns,deferred,deferred._template))
assert(deferred._hcm_encounter_reserve and #warnings==0)
local admitted,hidden,has_target=true,false,true
PhysicsWorld.raycast=function() return hidden end
local searches=0
POSITION_LOOKUP={player=vec(2000)}
Managers.state.main_path.ahead_unit=function() if has_target then return "player",position,vec(position) end end
Managers.state.main_path.nav_spawn_points=function() return {native=true} end
Managers.state.main_path.is_main_path_ready=function() return true end
Managers.state.main_path.travel_distance_from_position=function(_,p) return p[1] end
local side={valid_enemy_player_units_positions={POSITION_LOOKUP.player}}
Managers.state.extension.system=function(_,name)
 if name=="group_system" then return group_system end
 if name=="side_system" then return {get_side=function(_,id) assert(id==2);return side end} end
 return {trigger_wwise_event=function() end}
end
Managers.state.pacing.spawn_type_enabled=function() return admitted end
local queries=require("scripts/managers/main_path/utilities/spawn_point_queries")
queries.get_occluded_positions=function(nav,points,from,targets,offset,n,minimum,maximum)
 if minimum==35 then searches=searches+1 end
 assert(points.native and targets==side.valid_enemy_player_units_positions)
 assert(minimum==35 and maximum==120 and from[1]==position+60 or
  minimum==20 and maximum==60 and from[1]==POSITION_LOOKUP.player[1])
 assert(n==40)
 if hidden then return {vec(position+60)},1 end
end
function Vector3Box(value) local copy=vec(value[1],value[2],value[3]);return {unbox=function() return vec(copy[1],copy[2],copy[3]) end} end
setup_placement_engine()
Managers.state.pacing.roamer_traverse_logic=function() return placement_traverse end
deferred._expedition_setup_monster_loot=function() error("route missions must not create expedition loot") end
position=2000
for t=0,5 do update_hook(NativeMonster.update,deferred,1,t,2,1) end
local reserve=deferred._hcm_encounter_reserve
local remaining=reserve.monsters+reserve.patrols
admitted=false;update_hook(NativeMonster.update,deferred,1,100,2,1)
assert(searches==0 and reserve.monsters+reserve.patrols==remaining)
admitted=true;update_hook(NativeMonster.update,deferred,1,102,2,1)
assert(searches==1 and reserve.monsters+reserve.patrols==remaining)
update_hook(NativeMonster.update,deferred,.1,102.5,2,1);assert(searches==1)
host=false;update_hook(NativeMonster.update,deferred,1,104,2,1);assert(searches==1);host=true
has_target=false;update_hook(NativeMonster.update,deferred,1,106,2,1);assert(searches==1);has_target=true
deferred._disabled=true;update_hook(NativeMonster.update,deferred,1,108,2,1);assert(searches==1);deferred._disabled=false
hidden=true
local function opportunity(manager,t)
 update_hook(NativeMonster.update,manager,.05,t,2,1)
 local job=manager._hcm_encounter_reserve and manager._hcm_encounter_reserve.job
 if job then
  local deadline=t+19
  while not job.completed and t<deadline do t=t+.05;update_hook(NativeMonster.update,manager,.05,t,2,1) end
  assert(job.completed,"patrol admission did not finish")
  update_hook(NativeMonster.update,manager,.05,t+2.1,2,1)
 end
end
for t=110,310,40 do opportunity(deferred,t) end
for _,u in ipairs(units) do
 if u.params.spawn_source=="hcm_patrol" then
  assert(u.params.optional_aggro_state=="aggroed" and u.params.optional_target_unit=="player")
  assert(not BLACKBOARDS[u].patrol.should_patrol,"reserve still initialized a passive walking formation")
 end
end
local live=0;for _,record in ipairs(deferred._alive_monsters) do if HEALTH_ALIVE[record.spawned_unit] then live=live+1 end end
assert(live==3 and #reserve.groups==2,"overflow must respect both concurrency limits")
local held=reserve.monsters+reserve.patrols;local search_count=searches
update_hook(NativeMonster.update,deferred,1,350,2,1)
assert(reserve.monsters+reserve.patrols==held and searches==search_count)
for t=390,1400,40 do
 for _,record in ipairs(deferred._alive_monsters) do HEALTH_ALIVE[record.spawned_unit]=false end
 for _,group in ipairs(groups) do group.members={} end
 opportunity(deferred,t)
end
assert(not deferred._hcm_encounter_reserve)
local actual_monsters=0
for _,unit in ipairs(units) do if not unit.params.optional_group_id then actual_monsters=actual_monsters+1 end end
assert(actual_monsters==8 and #groups==6,"sparse map must eventually consume every requested encounter")
assert(deferred._pacing_type=="default" and deferred._currently_spawned_by_timer==nil)
local total=#units
for t=1401,1500 do update_hook(NativeMonster.update,deferred,1,t,2,1) end
assert(#units==total,"finite quotas must never create an endless reinforcements loop")
local unfinished=make_manager(1);assert(generate(NativeMonster._generate_spawns,unfinished,unfinished._template))
destroy_hook(unfinished);assert(not unfinished._hcm_encounter_reserve and #info_lines==0)
reserve_spawned_monsters=actual_monsters;reserve_spawned_patrols=#groups
-- Reproduce the three-BOT run: nine usable replenishment opportunities,
-- with a pending 11-boss/6-patrol plan. Both categories must get turns.
local Reserve=reserve_module
configure(5,6);units,groups={},{}
local fair=make_manager(1);assert(generate(NativeMonster._generate_spawns,fair,fair._template))
fair._monsters={};fair._boss_patrols={};fair._alive_monsters={}
Reserve.plan(fair,11,6)
update_hook(NativeMonster.update,fair,1,0,2,1)
local sequence={}
for turn=1,9 do
 for _,record in ipairs(fair._alive_monsters) do HEALTH_ALIVE[record.spawned_unit]=false end
 for _,group in ipairs(groups) do group.members={} end
 local r=fair._hcm_encounter_reserve;local before=r.monsters
 opportunity(fair,turn*40)
 sequence[#sequence+1]=r.monsters<before and "M" or "P"
end
local r=fair._hcm_encounter_reserve
assert(r.monsters==5 and r.patrols==3,"11:6 weighted reserve must serve 6 bosses and 3 patrols in nine opportunities")
fair_sequence=table.concat(sequence,",")
-- Very unequal quotas still give a ready patrol a turn within four successes.
units,groups={},{};fair._alive_monsters={};fair._hcm_next_patrol_member=nil;Reserve.plan(fair,100,1)
update_hook(NativeMonster.update,fair,1,0,2,1)
for turn=1,4 do
 for _,record in ipairs(fair._alive_monsters) do HEALTH_ALIVE[record.spawned_unit]=false end
 for _,group in ipairs(groups) do group.members={} end
 opportunity(fair,turn*40)
end
assert(fair._hcm_encounter_reserve.monsters==97 and fair._hcm_encounter_reserve.patrols==0)
-- A failed preferred spawn must preserve its quota and offer the other class.
units,groups={},{};fair._alive_monsters={}
fair._spawn_monster=function() end
Reserve.plan(fair,2,1)
update_hook(NativeMonster.update,fair,1,200,2,1)
opportunity(fair,220)
assert(fair._hcm_encounter_reserve.monsters==2 and fair._hcm_encounter_reserve.patrols==0)
assert(#groups==1 and #groups[1].members>0)
-- Neither failed spawn consumes a quota or advances the success interval.
local original_queue=B.queue_native_patrol;B.queue_native_patrol=function() end;units,groups={},{}
Reserve.plan(fair,2,1)
update_hook(NativeMonster.update,fair,1,300,2,1)
update_hook(NativeMonster.update,fair,1,320,2,1)
assert(fair._hcm_encounter_reserve.monsters==2 and fair._hcm_encounter_reserve.patrols==1)
assert(fair._hcm_encounter_reserve.next_at==320)
B.queue_native_patrol=original_queue
-- Consume expanded patrol compositions through the real native group spawner
-- at every level, rather than validating only the edited breed lists.
local Profile=load_mod_file("HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile")
patrol_curve={}
for level=1,10 do
 B.values.native_configuration_v3=Profile.values(level);Managers.state.game_session={};E.reset()
 units,groups={},{}
 local manager=make_manager(1)
 post_init_hook(function(self,level,template) self._template=template end,manager,"test_map",manager._template)
 assert(generate(NativeMonster._generate_spawns,manager,manager._template))
 manager._monsters={};manager._boss_patrols={};manager._alive_monsters={}
 Reserve.plan(manager,0,1)
 update_hook(NativeMonster.update,manager,1,0,2,1)
 opportunity(manager,20)
 assert(#groups==1 and manager._hcm_encounter_reserve.patrols==0)
 local count={common=0,elite=0}
 for _,unit in ipairs(groups[1].members) do
  local role=breeds[unit.breed].tags.elite and "elite" or "common";count[role]=count[role]+1
 end
 if level>1 then assert(count.common==patrol_curve[1].common and count.elite>=patrol_curve[level-1].elite) end
 patrol_curve[level]=count
end
assert(patrol_curve[10].elite==patrol_curve[1].elite*3)
-- Courtroom regression: native campaign safety does not pause "monsters".
-- HCM must honor the separate native safe-zone flag before starting its timer.
units,groups={},{};position=2000;POSITION_LOOKUP.player=vec(position)
side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP.player
local pacing=Managers.state.pacing
pacing.set_in_safe_zone=NativeSafePacing.set_in_safe_zone
pacing.get_in_safe_zone=NativeSafePacing.get_in_safe_zone
NativeSafeMode._restrict_spawning({},true)
assert(pacing:spawn_type_enabled("monsters") and pacing:get_in_safe_zone())
local guarded=make_manager(1);guarded._monsters={};guarded._boss_patrols={};guarded._alive_monsters={}
Reserve.plan(guarded,0,1)
local before_searches=searches
for t=0,100 do update_hook(function() end,guarded,1,t,2,1) end
assert(#units==0 and searches==before_searches and not guarded._hcm_encounter_reserve.next_at)
NativeSafeMode._restrict_spawning({},false)
update_hook(function() end,guarded,1,110,2,1)
update_hook(function() end,guarded,1,128,2,1)
assert(#units==0 and searches==before_searches)
update_hook(function() end,guarded,1,130,2,1)
assert(guarded._hcm_encounter_reserve.job and #units==0 and guarded._hcm_encounter_reserve.patrols==1)
update_hook(function() end,guarded,.01,130.01,2,1)
assert(#units==1 and guarded._hcm_encounter_reserve.patrols==1,"partially created patrol consumed a complete quota")
local locked=guarded._hcm_encounter_reserve.job.group_id
assert(groups[locked].locked)
B.finish_encounter_reserve(guarded)
assert(not groups[locked].locked and not guarded._hcm_patrol_jobs and not guarded._hcm_encounter_reserve)

-- The actual former native timed branch expands a hidden anchor into near
-- positions and creates the entire formation synchronously. Reproduce that
-- boundary fault, then feed the same output to the corrected admission path.
B.spawn_placement.finish()
local record={breed_list=base.boss_patrols.breed_lists,spawn_position=Vector3Box(vec(2060))}
GwNavQueries.flood_fill_from_position=function(_,pos,a,b,n,output)
 for i=1,n do output[i]=vec(2002+i*.1,0,15) end;return n
end
units,groups={},{}
NativeMonster._spawn_boss_patrol({_pacing_type="timer_based",_nav_world={},
 _currently_spawned_by_timer={boss_patrols={}},_expedition_setup_monster_loot=function() end},record,POSITION_LOOKUP.player,2)
assert(#units>1 and units[1].position[1]<2010,"former same-frame unsafe footprint was not reproduced")
units,groups={},{}
local corrected=make_manager(1)
local job=B.queue_native_patrol(corrected,record,2)
B.update_patrol_spawns(corrected,0,2,1)
for frame=1,119 do B.update_patrol_spawns(corrected,frame/60,2,1) end
assert(#units==0 and job.index==1 and not job.completed,"unsafe expanded member escaped the final guard")
PhysicsWorld.raycast=function() return false end
B.update_patrol_spawns(corrected,2.01,2,1)
assert(#units==0,"precomputed hidden points overrode current player LOS")
PhysicsWorld.raycast=function() return true end
B.finish_patrol_spawns(corrected)
-- A patrol with an unusable footprint cannot starve the ready monster class.
units,groups={},{};corrected=make_manager(1)
corrected._monsters={};corrected._boss_patrols={};corrected._alive_monsters={}
Reserve.plan(corrected,1,2)
update_hook(function() end,corrected,1,0,2,1)
update_hook(function() end,corrected,1,20,2,1)
assert(corrected._hcm_encounter_reserve.job and #units==0)
update_hook(function() end,corrected,1,40,2,1)
assert(corrected._hcm_encounter_reserve.monsters==0 and corrected._hcm_encounter_reserve.patrols==2 and #units==1)
B.finish_encounter_reserve(corrected)

local patrol_hook
for _,h in ipairs(hooks) do if h.target==class and h.name=="_spawn_boss_patrol" then patrol_hook=h.fn end end
assert(patrol_hook)
local ephemeral
GwNavQueries.flood_fill_from_position=function(_,pos,a,b,n,output)
 ephemeral=output;for i=1,n do output[i]=vec(pos[1]+i*.5) end;return n
end
patrol_frame_rates={}
for _,fps in ipairs({30,60,144}) do
 units,groups={},{}
 local manager=make_manager(1)
 local pending=patrol_hook(function() error("route patrol used the synchronous branch") end,manager,record,position,2)
 assert(#units==0 and pending)
 local times={}
 for frame=0,math.ceil(10*fps) do
  local t=frame/fps;local before=#units
  B.update_patrol_spawns(manager,t,2,1)
  B.update_patrol_spawns(manager,t,2,1)
  assert(#units-before<=1,"multiple patrol members created in one frame")
  if #units>before then times[#times+1]=t end
  if frame==0 then for _,v in ipairs(ephemeral) do v[1]=-9999 end end
  if pending.completed then break end
 end
 assert(pending.completed and #units==#pending.breeds and #groups[1].members==#units and not groups[1].locked)
 for i,u in ipairs(units) do
  assert(u.position[1]>=2035 and u.params.spawn_source=="hcm_patrol")
  if i>1 then
   assert(times[i]-times[i-1]>=.15-1e-9)
   assert(BLACKBOARDS[u].patrol.patrol_leader_unit==units[require("scripts/utilities/minion_patrols").get_follow_index(i)])
  end
 end
 patrol_frame_rates[fps]={members=#units,duration=times[#times]-times[1]}
end
-- Leaders use the verified actual player floor, not another main-path storey.
-- If the first member dies during staged deployment, the next living leader
-- must have native patrol index 1 (BtPatrolAction.enter's leader contract).
units,groups={},{};corrected=make_manager(1);job=B.queue_native_patrol(corrected,record,2)
POSITION_LOOKUP.player=vec(position,0,7)
side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP.player
B.update_patrol_spawns(corrected,0,2,1)
assert(#units==1 and units[1].walk_position[3]==7 and POSITION_LOOKUP.player[3]==7)
HEALTH_ALIVE[units[1]]=false
B.update_patrol_spawns(corrected,.2,2,1)
assert(#units==2 and BLACKBOARDS[units[2]].patrol.patrol_index==1)
assert(BLACKBOARDS[units[2]].patrol.auto_patrol and not BLACKBOARDS[units[2]].patrol.patrol_leader_unit)
B.finish_patrol_spawns(corrected)
POSITION_LOOKUP.player=vec(position);side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP.player
-- Each reserve member gets the current native target, including a target
-- change while a large group is still being admitted across frames.
units,groups={},{};corrected=make_manager(1)
job=B.queue_native_patrol(corrected,record,2,{groups={}})
B.update_patrol_spawns(corrected,0,2,1)
assert(units[1].params.optional_aggro_state=="aggroed" and units[1].params.optional_target_unit=="player")
local get_ahead=Managers.state.main_path.ahead_unit
POSITION_LOOKUP.other=vec(position)
Managers.state.main_path.ahead_unit=function() return "other",position,vec(position) end
B.update_patrol_spawns(corrected,.2,2,1)
assert(units[2].params.optional_aggro_state=="aggroed" and units[2].params.optional_target_unit=="other")
assert(not BLACKBOARDS[units[2]].patrol.should_patrol)
Managers.state.main_path.ahead_unit=get_ahead
B.finish_patrol_spawns(corrected)
-- Mid-deployment team movement cancels stale positions, without erasing the
-- remaining breed list or creating beside a player during the retry period.
units,groups={},{};corrected=make_manager(1);job=B.queue_native_patrol(corrected,record,2)
B.update_patrol_spawns(corrected,0,2,1);assert(#units==1)
position=2040;POSITION_LOOKUP.player=vec(position);side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP.player
B.update_patrol_spawns(corrected,.2,2,1)
assert(#units==1 and job.index==2 and not job.positions)
for frame=1,100 do B.update_patrol_spawns(corrected,.2+frame/60,2,1) end
assert(#units==1,"retry created at a stale near position")
B.update_patrol_spawns(corrected,2.21,2,1);assert(#units==2 and units[2].position[1]>=2075)
B.finish_patrol_spawns(corrected)
position=2000;POSITION_LOOKUP.player=vec(position);side.valid_enemy_player_units_positions[1]=POSITION_LOOKUP.player
host=false
local remote_manager=make_manager(1)
assert(patrol_hook(function() return "native" end,remote_manager,record,position,2)=="native" and not remote_manager._hcm_patrol_jobs)
host=true
math.random=original_random
''')
print('Native shared-section regression: requested 8 monsters + 6 patrols -> 3 + 0; extended plan -> 8 + 6 on existing authored positions: PASS')
print('Distinct positions and trigger gaps, finite overflow quotas, override restoration, mandatory objective metadata and default/remote passthrough: PASS')
print('Havoc additions, final placement warnings, zero overrides and native heat-based capacity/timer consumers: PASS')
print('Actual native update + spawn consumers with navigation/unit boundaries mocked:', L.globals().spawned_monsters, 'monsters,', L.globals().spawned_patrols, 'patrols,', L.globals().spawned_patrol_members, 'patrol members including', L.globals().spawned_elites, 'native-tagged elites: PASS')
print('Sparse map (3 points) consumes complete 8-monster/6-patrol plan through native hidden-position selection and spawn methods; no-position retry, finite quotas, 20-second intervals, 3-monster/2-extra-patrol limits and cleanup: PASS')

print("Nine usable opportunities for an 11-boss/6-patrol backlog:", L.globals().fair_sequence, "-> 6 bosses + 3 patrols; failed preferred spawn falls back without losing quota: PASS")
print('Actual native patrol spawns at all ten levels:', [dict(L.globals().patrol_curve[i].items()) for i in range(1,11)], 'PASS')

print('Courtroom safe-zone regression, actual unsafe native flood-fill reproduction, per-member distance/current LOS, boxed vector lifetime, delayed quota, team movement and cancellation: PASS')
print('Patrol admission at 30/60/144 FPS:', {fps: dict(L.globals().patrol_frame_rates[fps].items()) for fps in (30,60,144)}, 'PASS')
print('Verified player-floor destination, first-member death during staged patrol creation, active reserves and current target per member: PASS')
