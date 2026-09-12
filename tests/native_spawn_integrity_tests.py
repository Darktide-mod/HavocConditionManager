"""Reproduce queue wrap loss and deletion of unspawned roamers using game Lua."""
from native_harness import *

L.execute("""
function table.clear(t) for k in pairs(t) do t[k]=nil end end
function Vector3Box(v) local copy={v[1],v[2],v[3]};return {unbox=function() return {copy[1],copy[2],copy[3]} end} end
QuaternionBox=Vector3Box
Vector3={distance=function(a,b) return math.sqrt((a[1]-b[1])^2+(a[2]-b[2])^2+(a[3]-b[3])^2) end}
NativeMinion={};NativePacing={};NativeRoamer={}
HEALTH_ALIVE={};BLACKBOARDS={};POSITION_LOOKUP={}
local player={};POSITION_LOOKUP[player]={0,0,0}
side_system={side_by_unit={[player]={}}}
Managers.state.extension={system=function() return side_system end}
Managers.state.player_unit_spawn={alive_players=function() return {{player_unit=player}} end}
Managers.state.main_path={ahead_unit=function() return player,100 end,behind_unit=function() return player,90 end,path_type=function() return map_path_type end}
""")
def extract(source,marker):
    start=source.index(marker);end=source.index("\nend",start)+4
    return source[start:end]
for path,owner,target,names in [
 ("scripts/managers/minion/minion_spawn_manager.lua","MinionSpawnManager","NativeMinion",("init","queue_minion_to_spawn","_update_spawn_queue","total_allocated_num_enemies")),
 ("scripts/managers/pacing/pacing_manager.lua","PacingManager","NativePacing",("spawn_type_enabled",)),
 ("scripts/managers/pacing/roamer_pacing/roamer_pacing.lua","RoamerPacing","NativeRoamer",("update","_deactivate_roamer")),
]:
    source=(game/path).read_text(encoding="utf-8")
    prefix="local "+owner+"="+target+";local MINION_QUEUE_RING_BUFFER_SIZE=256;local HARD_ALLOCATED_LIMIT=145;local MAX_NUM_ROAMERS_ACTIVATIONS_PER_FRAME=1;local ACTIVE_TARGET_POSITIONS={};local MinionPatrols={update_roamer_patrols=function() end};"
    if target=="NativeRoamer":
        for helper in ("_roamer_is_passive","_roamer_is_aggroed"):
            prefix+=extract(source,"local function "+helper)+"\n"
    for name in names:
        L.execute(prefix+extract(source,owner+"."+name+" = function"))
load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks")
L.execute("""
local function hook(path,name)
 local target=require(path)
 for _,h in ipairs(hooks) do if h.target==target and h.name==name then return h.fn end end
 error(name)
end
local enqueue=hook("scripts/managers/minion/minion_spawn_manager","queue_minion_to_spawn")
local drain=hook("scripts/managers/minion/minion_spawn_manager","_update_spawn_queue")
local roamer_update=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","update")
local deactivate=hook("scripts/managers/pacing/roamer_pacing/roamer_pacing","_deactivate_roamer")
function new_spawn(fixed)
 local obj=setmetatable({records={}}, {__index=NativeMinion})
 NativeMinion.init(obj,123,{},nil)
 function obj:spawn_minion(breed,pos,rot,side,param)
  assert(pos and rot and param.sequence)
  self.records[#self.records+1]={breed=breed,position=pos,rotation=rot,side=side,sequence=param.sequence,source=param.spawn_source,group=param.optional_group_id,objective=param.optional_mission_objective_id}
  self._num_spawned_minions=self._num_spawned_minions+1
  if self.callback then self:callback() end
 end
 if fixed then
  obj.queue_minion_to_spawn=function(self,...) return enqueue(NativeMinion.queue_minion_to_spawn,self,...) end
  obj._update_spawn_queue=function(self) return drain(NativeMinion._update_spawn_queue,self) end
 end
 return obj
end
function add(obj,id)
 local entry=obj:queue_minion_to_spawn(id%3==0 and "elite" or "horde",{id,id+1,id+2},{id+3,0,0},2)
 entry.sequence=id;entry.spawn_source="combat_event";entry.optional_group_id=id+10;entry.optional_mission_objective_id="objective_"..id
 return entry
end
local broken=new_spawn(false)
for i=1,600 do add(broken,i) end
assert(broken._spawn_queue_size==600 and broken._spawn_queue[1].sequence==513)
local ok,err=pcall(function() for i=1,600 do broken:_update_spawn_queue() end end)
assert(not ok and tostring(err):find("position",1,true))
assert(#broken.records==256 and broken._spawn_queue_size==344)
queue_failure=tostring(err)

-- Wrapped ring growth keeps the original request tables and every extra field.
local fixed=new_spawn(true);local requests={}
for i=1,256 do requests[i]=add(fixed,i) end
for i=1,173 do fixed:_update_spawn_queue() end
for i=257,3000 do requests[i]=add(fixed,i) end
assert(fixed._hcm_spawn_queue_capacity==4096 and fixed._spawn_queue_size==2827)
assert(fixed._spawn_queue[1]==requests[174])
for i=174,3000 do
 assert(requests[i].sequence==i)
 local before=#fixed.records;fixed:_update_spawn_queue();assert(#fixed.records==before+1)
end
assert(fixed._spawn_queue_size==0 and fixed:total_allocated_num_enemies()==3000)
for i,record in ipairs(fixed.records) do
 assert(record.sequence==i and record.position[1]==i and record.position[3]==i+2 and record.rotation[1]==i+3)
 assert(record.breed==(i%3==0 and "elite" or "horde") and record.side==2)
 assert(record.source=="combat_event" and record.group==i+10 and record.objective=="objective_"..i)
 assert(not next(requests[i]))
end
fixed:_update_spawn_queue();assert(#fixed.records==3000)
-- The same grown ring remains valid after many complete wraps.
for batch=1,10 do
 for i=1,4200 do add(fixed,batch*10000+i) end
 for i=1,4200 do fixed:_update_spawn_queue() end
 assert(fixed._spawn_queue_size==0)
end

-- Enqueue from a spawn callback may itself grow/rebase the ring. Recursive
-- drain attempts must not spawn the current request twice or lose the new tail.
local nested=new_spawn(true)
for i=1,256 do add(nested,i) end
nested.callback=function(self)
 self.callback=nil
 for i=257,1600 do add(self,i) end
 self:_update_spawn_queue()
end
nested:_update_spawn_queue()
assert(#nested.records==1 and nested._spawn_queue_size==1599)
for i=2,1600 do nested:_update_spawn_queue() end
for i,r in ipairs(nested.records) do assert(r.sequence==i) end
assert(nested._spawn_queue_size==0)
-- A small queue is identical to native behavior, including returned parameters.
for _,local_host in ipairs({true,false}) do
 host=local_host;local a,b=new_spawn(false),new_spawn(true)
 for i=1,180 do add(a,i);add(b,i) end
 for i=1,180 do a:_update_spawn_queue();b:_update_spawn_queue() end
 assert(S.equal(a.records,b.records) and not b._hcm_spawn_queue_capacity)
end
host=true

local pm=setmetatable({_challenge_rating_thresholds={},_total_challenge_rating=0,_paused_spawn_types={},_allowed_spawn_types={roamers=true,specials=true},_heat_pacing={active=function() return false end}}, {__index=NativePacing})
Managers.state.pacing=pm
local allocation=new_spawn(true);Managers.state.minion_spawn=allocation
function new_roamers(fixed)
 local obj={_zones={},_roamer_template={spawn_distance=60},_roamers={},_num_roamers=3,_roamer_update_index=1,_roamer_lookup={},_patrol_data={patrols={{1,2}},active_patrols={}},activated={}}
 for i=1,3 do obj._roamers[i]={travel_distance=100+i,position=Vector3Box({i,0,0}),breed=i<3 and "elite" or "regular",patrol_id=i<3 and 1 or nil} end
 obj._update_faction_switch=function() end;obj._update_density_type_switch=function() end
 obj._handle_group_ambience_sfx=function() end;obj._despawn_roamer=function(_,unit) HEALTH_ALIVE[unit]=nil end
 obj._try_activate_roamer=function(self,roamer)
  local unit={};roamer.active=true;roamer.spawned_unit=unit;HEALTH_ALIVE[unit]=true
  BLACKBOARDS[unit]={perception={aggro_state="aggroed"}}
  self._roamer_lookup[unit]=roamer;self.activated[#self.activated+1]=roamer.breed;return true
 end
 obj._deactivate_roamer=fixed and function(self,roamer) return deactivate(NativeRoamer._deactivate_roamer,self,roamer) end or NativeRoamer._deactivate_roamer
 obj.update=fixed and function(self,...) return roamer_update(NativeRoamer.update,self,...) end or NativeRoamer.update
 return obj
end
for _,path_type in ipairs({"main_path","open"}) do
 map_path_type=path_type;allocation._num_spawned_minions=329;allocation._spawn_queue_size=178
 local allowed,reason=pm:spawn_type_enabled("roamers");assert(not allowed and reason=="Hard_allocated_limit_reached")
 B.values.native_configuration_v3={horde_size=5};E.reset()
 local old=new_roamers(false);old:update(.016,1,2,1);old:update(.016,2,2,1)
 assert(old._num_roamers==1 and #old._patrol_data.patrols[1]==0)
 local pending=new_roamers(true)
 local pending_checks=0;local guarded_deactivate=pending._deactivate_roamer
 pending._deactivate_roamer=function(self,r) pending_checks=pending_checks+1;return guarded_deactivate(self,r) end
 for i=1,90 do pending:update(.016,i,2,1) end
 assert(pending_checks==90,"Deferred checks exceeded the native per-frame work budget")
 assert(pending._num_roamers==3 and #pending._patrol_data.patrols[1]==2 and #pending.activated==0)
 assert(not pending._hcm_defer_unspawned_roamers)
 -- The hard limit remains in effect until actual live/pending counts recover.
 allocation._num_spawned_minions=30;allocation._spawn_queue_size=0
 for i=1,3 do pending:update(.016,100+i,2,1) end
 assert(#pending.activated==3 and pending.activated[1]=="elite" and pending.activated[2]=="elite")
 -- Active/dead cleanup still runs during a subsequent capacity pause.
 allocation._num_spawned_minions=329;local first=pending._roamers[1]
 HEALTH_ALIVE[first.spawned_unit]=nil;pending._roamer_update_index=1
 pending:update(.016,105,2,1)
 assert(pending._num_roamers==2 and #pending._patrol_data.patrols[1]==1)
 -- Local defaults and remote authority preserve the game's original behavior.
 B.values.native_configuration_v3={};E.reset();local defaults=new_roamers(true)
 defaults:update(.016,1,2,1);assert(defaults._num_roamers==2)
 B.values.native_configuration_v3={horde_size=5};E.reset();host=false;local remote=new_roamers(true)
 remote:update(.016,1,2,1);assert(remote._num_roamers==2);host=true
end
""")
print("Reproduced native queue overwrite and nil-position crash:",L.globals().queue_failure)
print("Growing native ring: 3,000-request burst, 42,000 wrapped requests, FIFO/params/boxed positions, one-per-update, reentrant growth and default/remote equivalence: PASS")
print("Actual native roamer update: capacity refusal erased pending elites; fix preserves plans on both path types, resumes after capacity returns and retains dead-unit cleanup: PASS")
