-- set_time only stages restore data. Match PlayerUnitAnimationState's ordered
-- time -> animation -> state restore before animation evaluation. This rebuilds
-- selected layers; it is not a generic playback-speed or blend-preserving API.
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
    return type(Unit.animation_get_time)=="function" and type(Unit.animation_set_time)=="function"
        and type(Unit.animation_get_state)=="function" and type(Unit.animation_get_animation)=="function"
        and type(Unit.animation_set_animation)=="function" and type(Unit.animation_set_state)=="function"
end
local function restore(snapshot)
    local targets,states,animations=snapshot.targets,snapshot.restore_states,snapshot.restore_animations
    table.clear(targets);table.clear(states);table.clear(animations)
    snapshot.restored=0;snapshot.failed=0
    for i=1,snapshot.count do
        local before,native_rate=snapshot.times[i],snapshot.native_rates[i]
        local failed=snapshot.failed_states[i]~=nil and snapshot.failed_states[i]==snapshot.states[i]
            and snapshot.failed_animations[i]==snapshot.animations[i]
        if not failed and before and native_rate and native_rate>0 and snapshot.states[i]~=nil and snapshot.animations[i]~=nil
            and snapshot.states[i]==snapshot.next_states[i] and snapshot.animations[i]==snapshot.next_animations[i]
            and snapshot.next_times[i] and math.abs(before-snapshot.next_times[i])<.0001 then
            targets[i]=before+snapshot.dt*native_rate*(snapshot.rate-1)
            states[i]=snapshot.states[i];animations[i]=snapshot.animations[i]
            snapshot.restored=snapshot.restored+1
        end
    end
    if snapshot.restored==0 then return end
    local unit,count=snapshot.unit,snapshot.count
    Unit.animation_set_time(unit,unpack(targets,1,count))
    Unit.animation_set_animation(unit,unpack(animations,1,count))
    -- nil leaves unrelated, inactive and transitioning layers untouched.
    Unit.animation_set_state(unit,unpack(states,1,count))
    snapshot.readback=Unit.animation_get_time(unit,snapshot.readback)
    for i=1,count do
        if targets[i] then
            local actual=snapshot.readback[i]
            if not actual or math.abs(actual-targets[i])>.0001 then
                snapshot.failed=snapshot.failed+1
                -- Do not rebuild an unsupported layer every frame. Wait for
                -- a different native state/clip before attempting it again.
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
    local function add(unit,rate)
        if unit and ALIVE[unit] and not seen[unit] and Unit.has_animation_state_machine(unit) then
            seen[unit]=true
            local snapshot=capture(records[unit],unit,rate,dt);records[unit]=snapshot
            restore(snapshot)
            snapshots[#snapshots+1]=snapshot
        end
    end
    for unit,record in pairs(current.moves)do
        if ALIVE[unit] then
            if record.brain and current.sync_motion then current:sync_motion(record)end
            local rate=current:animation_rate(record.brain)
            if rate~=1 then
                add(unit,rate)
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
                    add(victim,rate)
                    local first_person=ScriptUnit.has_extension(victim,"first_person_system")
                    if first_person then add(first_person:first_person_unit(),rate)end
                end
            end
        else current.moves[unit]=nil;records[unit]=nil end
    end
    for unit in pairs(records)do if not seen[unit] then records[unit]=nil end end
    return snapshots
end
function A.after(snapshots)
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
        end
    end
    return updated,layers,failed
end
return A
