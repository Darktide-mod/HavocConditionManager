-- Carry ownership through both native asynchronous queues for recovery.
-- Deferred spawn tickets own their batch context until native consumption.
local mod=get_mod("HavocConditionManager")
local Minion=require("scripts/managers/minion/minion_spawn_manager")
local Spawner=require("scripts/extension_systems/minion_spawner/minion_spawner_extension")
function mod.new_spawn_batch(source,side,target_side,event)
    return {source=source,side_id=side,target_side_id=target_side,event=event}
end
function mod.tag_spawn_request(entry)
    local batch=mod.current_spawn_batch
    if batch then entry._hcm_batch=batch end
    return entry
end
mod:hook(Minion,"spawn_minion",function(fn,self,breed,position,rotation,side,params,...)
    if not mod.has_local_gameplay_authority() then return fn(self,breed,position,rotation,side,params,...) end
    local previous=mod.current_spawn_batch
    local batch=params and params._hcm_batch or previous
    mod.current_spawn_batch=batch
    local ok,unit=pcall(fn,self,breed,position,rotation,side,params,...)
    mod.current_spawn_batch=previous
    if not ok then error(unit,0) end
    if unit and mod.diy_on_spawn then mod.diy_on_spawn(unit,breed,batch) end
    return unit
end)
mod:hook(Spawner,"add_spawns",function(fn,self,breeds,side,params,...)
    if mod.has_local_gameplay_authority() and mod.current_spawn_batch and params then
        params._hcm_batch=mod.current_spawn_batch
    end
    return fn(self,breeds,side,params,...)
end)
mod:hook(Spawner,"_spawn",function(fn,self,breed,data,...)
    local previous=mod.current_spawn_batch
    local batch=mod.has_local_gameplay_authority() and data and data._hcm_batch
    if batch then mod.current_spawn_batch=batch end
    local ok,result=pcall(fn,self,breed,data,...)
    mod.current_spawn_batch=previous
    if not ok then error(result,0) end
    return result
end)
function mod.finish_spawn_flow()
    mod.current_spawn_batch=nil
end
return true
