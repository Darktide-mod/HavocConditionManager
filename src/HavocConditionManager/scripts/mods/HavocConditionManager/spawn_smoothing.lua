-- Admission only: native spawners retain their queues, units and callbacks.
local mod=get_mod("HavocConditionManager")
local E=mod.template_runtime
local Spawner=require("scripts/extension_systems/minion_spawner/minion_spawner_extension")
local Horde=require("scripts/managers/pacing/horde_pacing/horde_pacing")
local function active() return mod.has_local_gameplay_authority() and E.config().changed end
local function trim(state,t)
    while state.first<=state.last do
        local entry=state.waiting[state.first]
        local extension=entry.extension
        if extension and extension._hcm_spawn_ticket==entry and extension._spawn_queue and extension._next_spawn_time and t-entry.seen<=1 then break end
        if extension and extension._hcm_spawn_ticket==entry then extension._hcm_spawn_ticket=nil end
        state.waiting[state.first]=nil
        state.first=state.first+1
    end
    if state.first>state.last then state.first=1;state.last=0 end
end
mod:hook(Spawner,"update",function(fn,self,unit,dt,t)
    if not self._is_server or not active() or not self._is_setup or not self._next_spawn_time or self._next_spawn_time>t then
        return fn(self,unit,dt,t)
    end
    local owner=self._owner_system
    local state=owner._hcm_spawn_admission
    if not state then state={waiting={},first=1,last=0};owner._hcm_spawn_admission=state end
    if state.t~=t then state.t=t;state.used=0 end
    trim(state,t)
    local entry=self._hcm_spawn_ticket
    if not entry then
        entry={extension=self};self._hcm_spawn_ticket=entry
        state.last=state.last+1;state.waiting[state.last]=entry
    end
    entry.seen=t
    if state.used>=2 or state.waiting[state.first]~=entry then return end
    state.used=state.used+1
    state.waiting[state.first]=nil;state.first=state.first+1
    self._hcm_spawn_ticket=nil
    -- Dequeue only after admission. Native update still owns spawn-delay,
    -- queue-id results, the last unit and the spawner completion event.
    return fn(self,unit,dt,t)
end)
mod:hook_safe(Spawner,"destroy",function(self)
    if self._hcm_spawn_ticket then self._hcm_spawn_ticket.extension=nil end
    self._hcm_spawn_ticket=nil
end)
-- Only ordinary/coordinated waves retry failed admission without consuming
-- their wave count. Trickle waves consume attempts even on failure: excluded.
mod:hook(Horde,"_spawn_horde_wave",function(fn,self,...)
    local spawn=Managers.state.minion_spawn
    if active() and spawn and (spawn._spawn_queue_size or 0)>=48 then return false end
    return fn(self,...)
end)
return true
