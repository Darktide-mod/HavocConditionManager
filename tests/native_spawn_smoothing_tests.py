"""Run actual spawner queues/updates and Buff allocation around admission hooks."""
from native_harness import *
import subprocess

def extract(path,owner,name):
    source=(game/path).read_text(encoding="utf-8-sig")
    start=source.index(owner+"."+name+" = function")
    return source[start:source.index("\nend",start)+4]

queue_path="scripts/extension_systems/minion_spawner/utilities/minion_spawner_queue.lua"
path=game/queue_path
if not path.exists():
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(subprocess.check_output(["git","show","HEAD:"+queue_path],cwd=game))
L.execute("""
NativeQueue={};NativeSpawner={};NativeHorde={};NativeBuff={}
ALIVE={};BLACKBOARDS={};Component={event=function(unit,name) unit.events[#unit.events+1]=name end}
function table.clear(t) for k in pairs(t) do t[k]=nil end end
table.set_readonly=function(t) return t end
""")
for owner,target,path,names,prefix in [
    ("MinionSpawnerQueue","NativeQueue",queue_path,("init","enqueue","dequeue","is_empty"),""),
    ("MinionSpawnerExtension","NativeSpawner","scripts/extension_systems/minion_spawner/minion_spawner_extension.lua",
     ("add_spawns","update","destroy"),"local DEFAULT_SPAWN_DELAY=0.25;"),
    ("HordePacing","NativeHorde","scripts/managers/pacing/horde_pacing/horde_pacing.lua",
     ("_update_horde_pacing",),"local HORDE_FAILED_WAIT_TIME=3;local CHALLENGE_RATING_FOR_NO_MOVE_TIMER_OVERRIDE=0;local TIME_SINCE_FORWARD_TRAVEL_CHANGE_MOVE_TIMER_OVERRIDE={60,60,60,30,30};"),
    ("BuffExtensionBase","NativeBuff","scripts/extension_systems/buff/buff_extension_base.lua",
     ("request_proc_event_param_table",),"local MAX_PROC_EVENTS=300;"),
]:
    for name in names: L.execute("local "+owner+"="+target+";"+prefix+extract(path,owner,name))
L.execute("""
log_records={}
Log={warning=function(tag,message,...) log_records[#log_records+1]={tag=tag,message=string.format(message,...)} end}
Managers.time={time=function() return clock_t end}
""")
load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/native_runtime_hooks")
L.execute("""
local function hook(target,name,safe)
 if type(target)=="string" then target=require(target) end
 for _,h in ipairs(hooks) do if h.target==target and h.name==name and (safe==nil or h.safe==safe) then return h.fn end end
 error("Missing hook: "..name)
end
local spawner_path="scripts/extension_systems/minion_spawner/minion_spawner_extension"
local admit=hook(spawner_path,"update")
local destroyed=hook(spawner_path,"destroy")
local wave=hook("scripts/managers/pacing/horde_pacing/horde_pacing","_spawn_horde_wave")
local function configure(changed)
 host=true;B.values.native_configuration_v3=changed and {horde_waves=6} or {}
 Managers.state.game_session={};E.reset()
end
local function spawn_set(fixed,count,delay)
 local owner={enable_update_function=function() end,disable_update_function=function() end}
 local rows={}
 for i=1,count do
  local queue=setmetatable({}, {__index=NativeQueue});queue:init()
  local unit={events={}}
  local self=setmetatable({_unit=unit,_is_server=true,_is_setup=true,_owner_system=owner,
   _spawn_queue=queue,_spawned_minions_by_queue_id={},records={}}, {__index=NativeSpawner})
  function self:_spawn(breed,data)
   local spawned={breed=breed,objective=data.mission_objective_id,group=data.group_id,source=data.optional_owning_auto_event_id}
   self.records[#self.records+1]=spawned
   return spawned
  end
  self.fixed=fixed
  self.ids={}
  for j=1,2 do
   self.ids[j]=self:add_spawns({"elite_"..i.."_"..j,"special_"..i.."_"..j,"horde_"..i.."_"..j},2,
    {mission_objective_id="objective",group_id=i,optional_owning_auto_event_id=999,optional_spawn_delay=delay})
  end
  rows[i]=self
 end
 return rows,owner
end
local function tick(rows,dt,t)
 local delta=0
 for _,s in ipairs(rows) do
  local before=#s.records
  if s.fixed then admit(NativeSpawner.update,s,s._unit,dt,t) else NativeSpawner.update(s,s._unit,dt,t) end
  delta=delta+#s.records-before
 end
 return delta
end
configure(true)
local original=spawn_set(false,40,0)
assert(tick(original,1/60,0)==40)
local fixed,owner=spawn_set(true,40,0)
assert(tick(fixed,1/60,0)==2)
local total,peak=2,2
for frame=1,300 do local n=tick(fixed,1/60,frame/60);total=total+n;peak=math.max(peak,n) end
assert(total==240 and peak==2)
for i,s in ipairs(fixed) do
 assert(#s.records==6 and s._next_spawn_time==nil and s._hcm_spawn_ticket==nil)
 assert(#s._unit.events==2 and s._unit.events[2]=="minion_spawner_spawning_done")
 for j=1,2 do
  local units=s._spawned_minions_by_queue_id[s.ids[j]]
  assert(#units==3 and units[1].breed=="elite_"..i.."_"..j and units[2].breed=="special_"..i.."_"..j)
  for _,u in ipairs(units) do assert(u.objective=="objective" and u.group==i and u.source==999) end
 end
end
assert(owner._hcm_spawn_admission.last-owner._hcm_spawn_admission.first<1)
-- Persistent demand cannot starve spawners later in the native iteration order.
fixed=spawn_set(true,40,0)
for frame=1,300 do
 tick(fixed,1/60,frame/60)
 for _,s in ipairs(fixed) do
  if #s._spawn_queue._queue<2 then s:add_spawns({"extra"},2,{group_id=1,optional_spawn_delay=0}) end
 end
end
for _,s in ipairs(fixed) do assert(#s.records>=10) end
-- Default settings and remote clients keep their native concurrent update.
configure(false);local defaults=spawn_set(true,40,0);assert(tick(defaults,.016,0)==40)
configure(true);host=false;local remote=spawn_set(true,40,0);assert(tick(remote,.016,0)==40);host=true
-- Destroying a waiting spawner and pausing another must not block the queue.
fixed,owner=spawn_set(true,8,0);tick(fixed,.016,0)
NativeSpawner.destroy(fixed[3]);destroyed(fixed[3])
for frame=1,200 do
 for i,s in ipairs(fixed) do if i~=3 and i~=4 then admit(NativeSpawner.update,s,s._unit,.016,frame*.016) end end
end
for i,s in ipairs(fixed) do if i~=3 and i~=4 then assert(#s.records==6) end end
for frame=201,300 do admit(NativeSpawner.update,fixed[4],fixed[4]._unit,.016,frame*.016) end
assert(#fixed[4].records==6)
-- Empty queues still wait for their final unit to exit before completion.
local one=spawn_set(true,1,.25);local s=one[1]
for frame=1,100 do tick(one,.016,frame*.016) end
local last=s._last_spawned_minion
ALIVE[last]=true;BLACKBOARDS[last]={spawn={is_exiting_spawner=true}};s._next_spawn_time=2
tick(one,.016,2);assert(s._next_spawn_time==2)
BLACKBOARDS[last].spawn.is_exiting_spawner=false
tick(one,.016,2.1);assert(s._next_spawn_time==nil)
-- A pending ordinary wave retries through the actual native state machine.
Managers.state.minion_spawn={_spawn_queue_size=48}
Managers.state.pacing={get_ramp_up_frequency_modifier=function() return 1 end,num_aggroed_monsters=function() return 0 end,total_challenge_rating=function() return 0 end}
Managers.state.difficulty={get_table_entry_by_resistance=function() return 30 end}
Managers.state.mutator={mutator=function() return nil end}
local native_calls=0
local h={_template={num_waves={far_vector_horde=6},time_between_waves=5},_traveled_this_frame=0,
 _time_since_forward_travel_changed=0,_horde_started=true,_horde_timer=3,_rate_modifier=1,
 _current_wave=1,_next_horde_at=3,_current_horde_type="far_vector_horde"}
function h:_spawn_horde_wave(...) return wave(function() native_calls=native_calls+1;return true,nil,nil,nil end,self,...) end
NativeHorde._update_horde_pacing(h,0,.016,1,2)
assert(native_calls==0 and h._current_wave==1 and h._next_horde_at==3)
Managers.state.minion_spawn._spawn_queue_size=47;h._horde_timer=3
NativeHorde._update_horde_pacing(h,3,.016,1,2)
assert(native_calls==1 and h._current_wave==2 and h._next_horde_at==5)
for _,item in ipairs(hooks) do assert(item.name~="_spawn_trickle_horde_wave") end
-- Aggregation leaves the actual Buff allocator and all 300 table identities intact.
local log_hook=hook(Log,"warning")
local raw_log=Log.warning
Log.warning=function(...) return log_hook(raw_log,...) end
clock_t=0;log_records={}
local buff=setmetatable({_num_params_table_in_use=0,_param_tables_start_index_reference=1,_proc_event_param_tables={}}, {__index=NativeBuff})
local tables={}
for i=1,300 do tables[i]=buff:request_proc_event_param_table();assert(tables[i]) end
for i=1,2700 do assert(buff:request_proc_event_param_table()==nil) end
assert(#log_records==1 and buff._num_params_table_in_use==300)
local pacing=require("scripts/managers/pacing/pacing_manager")
local update=hook(pacing,"update",false)
local original_clear=E.clear_context;local cleared,native_updated=0,0
E.clear_context=function() cleared=cleared+1;original_clear() end
local result=update(function(_,dt,t)
 assert(cleared==1 and dt==.016 and t==1)
 native_updated=native_updated+1;return "updated"
end,{},.016,1)
assert(result=="updated" and native_updated==1 and cleared==1)
E.clear_context=original_clear
assert(#log_records==2 and log_records[2].message:find("2699 additional",1,true))
Log.warning("OtherSystem","Keep %s", "this");assert(#log_records==3 and log_records[3].message=="Keep this")
host=false;for i=1,3 do buff:request_proc_event_param_table() end;assert(#log_records==6);host=true
for i=1,300 do assert(buff._proc_event_param_tables[i]==tables[i]) end
clock_t=1.2;buff:request_proc_event_param_table()
hook(pacing,"destroy",true)()
assert(#log_records==7 and log_records[7].message:find("1 additional",1,true))
clock_t=2;buff:request_proc_event_param_table();buff:request_proc_event_param_table()
B.reset_native_spawn_scaling()
assert(#log_records==9 and log_records[9].message:find("1 additional",1,true))
clock_t=0;buff:request_proc_event_param_table()
assert(#log_records==10 and log_records[10].message=="Out of proc event tables, ignoring proc!")
""")
print("Native spawner updates: 40 concurrent spawns -> at most 2; 240/240 retained with FIFO results, source metadata and completion callbacks: PASS")
print("Sustained demand fairness, destroyed/paused spawners, original delays, final-unit exit, native defaults and remote behavior: PASS")
print("Native horde retry retains pending wave; trickle attempts untouched; native Buff 300 boundary preserved with 2700 warnings summarized in 2 writes: PASS")
