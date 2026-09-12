-- Track native creation events so recovery retains the correct ownership.
local mod=get_mod("HavocConditionManager")
local registered
local listener={}
function listener:on_minion_spawned(unit)
    if unit and mod.has_local_gameplay_authority() and mod.track_redeployed_unit then
        mod.track_redeployed_unit(unit)
    end
end
mod.start_spawn_tracking=function()
    local events=Managers.event
    if not mod.has_local_gameplay_authority() or not events or not events.register or events==registered then return end
    if registered then mod.finish_spawn_tracking() end
    events:register(listener,"minion_unit_spawned","on_minion_spawned")
    registered=events
end
mod.finish_spawn_tracking=function()
    if registered then registered:unregister(listener,"minion_unit_spawned");registered=nil end
end
return true
