-- Preserve native event doors and timing. Only carry ownership through their
-- asynchronous spawn queues so completed-event leftovers can be recognized.
local mod=get_mod("HavocConditionManager")
local Terror=require("scripts/managers/terror_event/terror_event_manager")
local function invoke(fn,batch,...)
    local previous=mod.current_spawn_batch
    mod.current_spawn_batch=batch
    local ok,a,b,c,d,e=pcall(fn,...)
    mod.current_spawn_batch=previous
    if not ok then error(a,0) end
    return a,b,c,d,e
end
function mod.run_event_spawn_node(fn,node,scratchpad,t,dt)
    if not mod.has_local_gameplay_authority() or scratchpad.started_spawn or not node.spawner_group then
        return fn(node,scratchpad,t,dt)
    end
    local pacing=Managers.state.pacing
    local batch=scratchpad._hcm_spawn_batch
    if not batch then
        batch=mod.new_spawn_batch("mission_spawner",pacing._side_id,pacing._target_side_id,node.spawner_group)
        batch.protected_objective=node.mission_objective_id
        scratchpad._hcm_spawn_batch=batch
    end
    return invoke(fn,batch,node,scratchpad,t,dt)
end
mod:hook(Terror,"_update_terror_trickle",function(fn,self,dt,t)
    local data=self._terror_trickle_data
    if not mod.has_local_gameplay_authority() or not data or not data.active or not data.spawner_group or
        not data.wave_timer or data.wave_timer>dt then return fn(self,dt,t) end
    local batch=data._hcm_spawn_batch
    if not batch or batch.event~=data.spawner_group then
        batch=mod.new_spawn_batch("mission_spawner",data.spawn_side_id,data.target_side_id,data.spawner_group)
        data._hcm_spawn_batch=batch
    end
    local wave=data.wave_counter
    local a,b,c,d,e=invoke(fn,batch,self,dt,t)
    if data.wave_counter~=wave then data._hcm_spawn_batch=nil end
    return a,b,c,d,e
end)
return true
