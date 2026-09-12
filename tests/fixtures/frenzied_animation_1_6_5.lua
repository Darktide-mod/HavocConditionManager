-- Advance existing clip and custom-blend players before world evaluation.
-- Never reconstruct a layer: doing so discards the outgoing transition.
local Clock=require("./native_clock.lua")
local A={}
local function capture(snapshot,unit,rate,dt)
    snapshot=snapshot or {times={},states={},animations={},next_times={},next_states={},next_animations={},
        native_rates={},targets={},restore_states={},restore_animations={},readback={},failed_states={},failed_animations={}}
    snapshot.unit,snapshot.rate,snapshot.dt=unit,rate,dt
    snapshot.times,snapshot.count=Unit.animation_get_time(unit,snapshot.times)
    snapshot.states=Unit.animation_get_state(unit,snapshot.states)
    snapshot.animations=Unit.animation_get_animation(unit,snapshot.animations)
    return snapshot
end
function A.available()
    if type(Unit.animation_get_time)~="function" or type(Unit.animation_get_state)~="function"
        or type(Unit.animation_get_animation)~="function" then return false,"animation getters unavailable" end
    return Clock.available()
end
local function advance(snapshot)
    local targets,states,animations=snapshot.targets,snapshot.restore_states,snapshot.restore_animations
    table.clear(targets);table.clear(states);table.clear(animations)
    snapshot.restored=0;snapshot.failed=0;snapshot.reason=nil
    for i=1,snapshot.count do
        local before,native_rate=snapshot.times[i],snapshot.native_rates[i]
        local failed=snapshot.failed_states[i]~=nil and snapshot.failed_states[i]==snapshot.states[i]
            and snapshot.failed_animations[i]==snapshot.animations[i]
        if not failed and before and native_rate and native_rate>0 and snapshot.states[i]~=nil and snapshot.animations[i]~=nil
            and snapshot.states[i]==snapshot.next_states[i] and snapshot.animations[i]==snapshot.next_animations[i]
            and snapshot.next_times[i] and math.abs(before-snapshot.next_times[i])<.0001 then
            local target,why=Clock.advance(snapshot.unit,i,before,before+snapshot.dt*native_rate*(snapshot.rate-1),snapshot.count)
            if target then
                targets[i]=target;states[i]=snapshot.states[i];animations[i]=snapshot.animations[i]
                snapshot.restored=snapshot.restored+1
            elseif target==nil then
                snapshot.failed=snapshot.failed+1;snapshot.reason=why
                snapshot.failed_states[i]=snapshot.states[i];snapshot.failed_animations[i]=snapshot.animations[i]
            end
        end
    end
    if snapshot.restored==0 then return end
    local unit,count=snapshot.unit,snapshot.count
    snapshot.readback=Unit.animation_get_time(unit,snapshot.readback)
    snapshot.readback_states=Unit.animation_get_state(unit,snapshot.readback_states)
    snapshot.readback_animations=Unit.animation_get_animation(unit,snapshot.readback_animations)
    for i=1,count do
        if targets[i] then
            local actual=snapshot.readback[i]
            if not actual or math.abs(actual-targets[i])>.0001 or snapshot.readback_states[i]~=states[i]
                or snapshot.readback_animations[i]~=animations[i] then
                snapshot.failed=snapshot.failed+1
                snapshot.reason="public clock/state/clip readback mismatch"
                snapshot.failed_states[i]=snapshot.states[i]
                snapshot.failed_animations[i]=snapshot.animations[i]
            end
        end
    end
end
function A.before(current,world,dt)
    if dt<=0 or world~=current.world or not World.get_data(world,"active") or World.get_data(world,"paused") then return end
    -- Keep the per-unit buffers between frames. A horde must not allocate
    -- six new Lua arrays per enemy on every animation update.
    local snapshots=current.animation_snapshots or {};current.animation_snapshots=snapshots
    local seen=current.animation_seen or {};current.animation_seen=seen
    local records=current.animation_records or {};current.animation_records=records
    table.clear(snapshots);table.clear(seen)
    local function add(unit,rate,label)
        if unit and ALIVE[unit] and not seen[unit] and Unit.has_animation_state_machine(unit) then
            seen[unit]=true
            local snapshot=capture(records[unit],unit,rate,dt);records[unit]=snapshot
            snapshot.label=label
            advance(snapshot)
            snapshots[#snapshots+1]=snapshot
        end
    end
    for unit,record in pairs(current.moves)do
        if ALIVE[unit] then
            if record.brain and current.sync_motion then current:sync_motion(record)end
            local rate=current:animation_rate(record.brain)
            if rate~=1 then
                local brain=record.brain
                local label=(brain and brain._breed and brain._breed.name or "unknown").."/"
                    ..(brain and brain._running_leaf_node and brain._running_leaf_node.tree_node[1] or "unknown")
                add(unit,rate,label)
                -- Only an actual paired victim, still owned by this minion,
                -- shares the attack animation clock. Free players never do.
                local pad=record.brain and record.brain._scratchpad
                local victim=pad and (pad.grabbed_target or pad.grabbed_unit or pad.target_unit
                    or pad.pounce_component and pad.pounce_component.pounce_target
                    or pad.perception_component and pad.perception_component.target_unit)
                local data=victim and ALIVE[victim] and ScriptUnit.has_extension(victim,"unit_data_system")
                local breed=data and data:breed()
                local disabled=breed and breed.breed_type=="player" and data:read_component("disabled_character_state")
                if disabled and disabled.disabling_unit==unit then
                    add(victim,rate,label.."/victim")
                    local first_person=ScriptUnit.has_extension(victim,"first_person_system")
                    if first_person then add(first_person:first_person_unit(),rate,label.."/first_person")end
                end
            end
        else current.moves[unit]=nil;records[unit]=nil end
    end
    for unit in pairs(records)do if not seen[unit] then records[unit]=nil end end
    return snapshots
end
function A.after(snapshots,current)
    local updated,layers,failed=0,0,0
    for _,snapshot in ipairs(snapshots or {})do
        local unit=snapshot.unit
        if ALIVE[unit] then
            local times,count=Unit.animation_get_time(unit,snapshot.next_times)
            local states=Unit.animation_get_state(unit,snapshot.next_states)
            local animations=Unit.animation_get_animation(unit,snapshot.next_animations)
            snapshot.next_times,snapshot.next_states,snapshot.next_animations=times,states,animations
            local verified_layers=0
            table.clear(snapshot.native_rates)
            for i=1,count do
                local target=snapshot.targets[i]
                local before=target and snapshot.readback[i] or snapshot.times[i]
                local now=times[i]
                -- A transition or loop establishes a new playhead. Do not
                -- import elapsed time from an unrelated animation/layer.
                if before and now and now>=before and states[i]==snapshot.states[i]
                    and animations[i]==snapshot.animations[i] then
                    snapshot.native_rates[i]=(now-before)/snapshot.dt
                    if target and now>before and math.abs(before-target)<.0001 then verified_layers=verified_layers+1 end
                end
            end
            if verified_layers>0 then updated=updated+1;layers=layers+verified_layers end
            failed=failed+snapshot.failed
            if current and current.log and (verified_layers>0 or snapshot.failed>0) then
                local logged=current.animation_diagnostics or {};current.animation_diagnostics=logged
                local status=snapshot.failed>0 and "failed" or "verified"
                local key=snapshot.label.."/"..status
                if not logged[key] then
                    logged[key]=true
                    current.log(string.format("[Frenzied assault] animation_clock=%s unit_action=%s rate=%.2f layers=%d failed=%d method=in_place reason=%s",
                        status,snapshot.label,snapshot.rate,verified_layers,snapshot.failed,snapshot.reason or "none"))
                end
            end
        end
    end
    return updated,layers,failed
end
return A
