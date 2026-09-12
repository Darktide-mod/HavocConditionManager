-- Select per-unit policy; native evaluation advances clocks, blends,
-- events and root motion with scaled dt. No per-layer seeks or getters.
local Native=require("./native_timestep.lua")
local A={cleanup=Native.cleanup}
function A.available()
    local ok,why=Native.available()
    if ok then Native.complete_trace()end -- Disable diagnostic atomic writes from the first frame.
    return ok,why
end
local function add(current,unit,rate,brain)
    local seen,records=current.animation_seen,current.animation_records
    if not unit or not ALIVE[unit] or seen[unit] or not Unit.has_animation_state_machine(unit) then return end
    seen[unit]=true
    local record=records[unit] or {};records[unit]=record
    local binding,why=Native.bind(unit,rate,record)
    if not binding and current.log and record.last_error~=why then
        record.last_error=why
        local node=brain and brain._running_leaf_node
        local label=(brain and brain._breed and brain._breed.name or "unknown").."/"..(node and node.tree_node[1] or "unknown")
        current.log("[Frenzied assault] native_timestep=binding_failed unit_action="..label.." reason="..tostring(why))
    end
end
function A.before(current,world,dt)
    if dt<=0 or world~=current.world or not World.get_data(world,"active") or World.get_data(world,"paused") then return end
    local seen=current.animation_seen or {};current.animation_seen=seen
    local records=current.animation_records or {};current.animation_records=records
    local victims=current.animation_victims or {};current.animation_victims=victims
    table.clear(seen);table.clear(victims)
    Native.begin()
    for unit,record in pairs(current.moves)do
        if ALIVE[unit] then
            local brain=record.brain
            local rate=current:animation_rate(brain)
            if rate~=1 then
                add(current,unit,rate,brain)
                local pad=brain and brain._scratchpad
                local victim=pad and (pad.grabbed_target or pad.grabbed_unit or pad.target_unit
                    or pad.pounce_component and pad.pounce_component.pounce_target
                    or pad.perception_component and pad.perception_component.target_unit)
                if victim and ALIVE[victim] then
                    -- Many enemies target the same player. Resolve ownership
                    -- once per synchronous pass; never retain it across frames.
                    local owner=victims[victim]
                    if owner==nil then
                        local data=ScriptUnit.has_extension(victim,"unit_data_system")
                        local breed=data and data:breed()
                        local disabled=breed and breed.breed_type=="player" and data:read_component("disabled_character_state")
                        owner=disabled and disabled.disabling_unit or false
                        victims[victim]=owner
                    end
                    if owner==unit then
                        add(current,victim,rate,brain)
                        local first_person=ScriptUnit.has_extension(victim,"first_person_system")
                        if first_person then add(current,first_person:first_person_unit(),rate,brain)end
                    end
                end
            end
        else current.moves[unit]=nil;records[unit]=nil end
    end
    for unit in pairs(records)do if not seen[unit] then records[unit]=nil end end
    table.clear(victims)
    Native.commit()
    return true
end
function A.after()
    Native.finish()
end
return A
