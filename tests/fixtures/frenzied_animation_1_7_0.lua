-- Select per-unit policy; native evaluation advances clocks, blends,
-- events and root motion with scaled dt. No per-layer seeks or getters.
local Native=require("./native_timestep.lua")
local A={available=Native.available,cleanup=Native.cleanup}
local function add(current,unit,rate,label)
    local seen,records,snapshots=current.animation_seen,current.animation_records,current.animation_snapshots
    if not unit or not ALIVE[unit] or seen[unit] or not Unit.has_animation_state_machine(unit) then return end
    seen[unit]=true
    local record=records[unit] or {};records[unit]=record
    local binding,why=Native.bind(unit,rate,record)
    if binding then
        record.unit,record.rate,record.label=unit,rate,label
        snapshots[#snapshots+1]=record
    elseif current.log and record.last_error~=why then
        record.last_error=why
        current.log("[Frenzied assault] native_timestep=binding_failed unit_action="..label.." reason="..tostring(why))
    end
end
function A.before(current,world,dt)
    if dt<=0 or world~=current.world or not World.get_data(world,"active") or World.get_data(world,"paused") then return end
    local snapshots=current.animation_snapshots or {};current.animation_snapshots=snapshots
    local seen=current.animation_seen or {};current.animation_seen=seen
    local records=current.animation_records or {};current.animation_records=records
    table.clear(snapshots);table.clear(seen)
    Native.begin()
    for unit,record in pairs(current.moves)do
        if ALIVE[unit] then
            local rate=current:animation_rate(record.brain)
            if rate~=1 then
                local brain=record.brain;local node=brain and brain._running_leaf_node
                if not record.animation_label or record.animation_node~=node then
                    record.animation_node=node
                    record.animation_label=(brain and brain._breed and brain._breed.name or "unknown").."/"
                        ..(node and node.tree_node[1] or "unknown")
                    record.victim_label=record.animation_label.."/victim"
                    record.first_person_label=record.animation_label.."/first_person"
                end
                add(current,unit,rate,record.animation_label)
                local pad=brain and brain._scratchpad
                local victim=pad and (pad.grabbed_target or pad.grabbed_unit or pad.target_unit
                    or pad.pounce_component and pad.pounce_component.pounce_target
                    or pad.perception_component and pad.perception_component.target_unit)
                local data=victim and ALIVE[victim] and ScriptUnit.has_extension(victim,"unit_data_system")
                local breed=data and data:breed()
                local disabled=breed and breed.breed_type=="player" and data:read_component("disabled_character_state")
                if disabled and disabled.disabling_unit==unit then
                    add(current,victim,rate,record.victim_label)
                    local first_person=ScriptUnit.has_extension(victim,"first_person_system")
                    if first_person then add(current,first_person:first_person_unit(),rate,record.first_person_label)end
                end
            end
        else current.moves[unit]=nil;records[unit]=nil end
    end
    for unit in pairs(records)do if not seen[unit] then records[unit]=nil end end
    Native.commit()
    return snapshots
end
function A.after(snapshots,current)
    Native.finish()
    if current and current.animation_confirmed then return 0,0,0 end
    local observed=0
    for _,record in ipairs(snapshots or {})do
        if Native.observed(record) then observed=observed+1 end
    end
    if observed>0 then
        if current and current.log then
            current.log(string.format("[Frenzied assault] native_timestep=observed units=%d state_machine=scaled blender=scaled playback=scaled method=engine_dt",observed))
        end
        if current then current.animation_confirmed=true end
        Native.complete_trace()
    end
    return observed,0,0
end
return A
