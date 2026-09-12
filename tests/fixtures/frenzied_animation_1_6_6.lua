-- Advance existing clip and custom-blend players before world evaluation.
-- Never reconstruct a layer: doing so discards the outgoing transition.
local Clock=require("./native_clock.lua")
local A={}
local function capture(snapshot,unit,rate,dt)
    snapshot=snapshot or {times={},states={},animations={},next_times={},next_states={},next_animations={},
        native_rates={},targets={},clock_context={},failed_states={},failed_animations={}}
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
    local targets=snapshot.targets
    table.clear(targets)
    snapshot.restored=0;snapshot.failed=0;snapshot.reason=nil
    local prepared,context,prepare_reason=false,nil,nil
    for i=1,snapshot.count do
        local before,native_rate=snapshot.times[i],snapshot.native_rates[i]
        local failed=snapshot.failed_states[i]~=nil and snapshot.failed_states[i]==snapshot.states[i]
            and snapshot.failed_animations[i]==snapshot.animations[i]
        if not failed and before and native_rate and native_rate>0 and snapshot.states[i]~=nil and snapshot.animations[i]~=nil
            and snapshot.states[i]==snapshot.next_states[i] and snapshot.animations[i]==snapshot.next_animations[i]
            and snapshot.next_times[i] and math.abs(before-snapshot.next_times[i])<.0001 then
            if not prepared then
                prepared=true
                context,prepare_reason=Clock.prepare(snapshot.unit,snapshot.count,snapshot.clock_context)
            end
            local target,why
            if context then
                target,why=Clock.advance_prepared(context,i,before,before+snapshot.dt*native_rate*(snapshot.rate-1))
            else why=prepare_reason end
            if target then
                targets[i]=target
                snapshot.restored=snapshot.restored+1
            elseif target==nil then
                snapshot.failed=snapshot.failed+1;snapshot.reason=why
                snapshot.failed_states[i]=snapshot.states[i];snapshot.failed_animations[i]=snapshot.animations[i]
            end
        end
    end
    -- Each seek already verifies its live clock, state pointer and layer
    -- count. The post-world public getters below verify state/clip continuity;
    -- repeating all three whole-unit getters here adds no engine evaluation.
end
local function add(current,unit,rate,label,dt)
    local seen,records,snapshots=current.animation_seen,current.animation_records,current.animation_snapshots
    if unit and ALIVE[unit] and not seen[unit] and Unit.has_animation_state_machine(unit) then
        seen[unit]=true
        local snapshot=capture(records[unit],unit,rate,dt);records[unit]=snapshot
        if snapshot.label~=label then
            snapshot.label=label;snapshot.verified_logged=nil;snapshot.failed_logged=nil
        end
        advance(snapshot)
        snapshots[#snapshots+1]=snapshot
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
    Clock.begin_frame()
    for unit,record in pairs(current.moves)do
        if ALIVE[unit] then
            if record.brain and current.sync_motion then current:sync_motion(record)end
            local rate=current:animation_rate(record.brain)
            if rate~=1 then
                local brain=record.brain
                local node=brain and brain._running_leaf_node
                if not record.animation_label or record.animation_node~=node then
                    record.animation_node=node
                    record.animation_label=(brain and brain._breed and brain._breed.name or "unknown").."/"
                        ..(node and node.tree_node[1] or "unknown")
                    record.victim_label=record.animation_label.."/victim"
                    record.first_person_label=record.animation_label.."/first_person"
                end
                add(current,unit,rate,record.animation_label,dt)
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
                    add(current,victim,rate,record.victim_label,dt)
                    local first_person=ScriptUnit.has_extension(victim,"first_person_system")
                    if first_person then add(current,first_person:first_person_unit(),rate,record.first_person_label,dt)end
                end
            end
        else current.moves[unit]=nil;records[unit]=nil end
    end
    Clock.end_frame()
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
                local before=target or snapshot.times[i]
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
                local flag=snapshot.failed>0 and "failed_logged" or "verified_logged"
                if not snapshot[flag] then
                    snapshot[flag]=true
                    local key=snapshot.label.."/"..status
                    if not logged[key] then
                        logged[key]=true
                        current.log(string.format("[Frenzied assault] animation_clock=%s unit_action=%s rate=%.2f layers=%d failed=%d method=in_place reason=%s",
                            status,snapshot.label,snapshot.rate,verified_layers,snapshot.failed,snapshot.reason or "none"))
                    end
                end
            end
        end
    end
    return updated,layers,failed
end
return A
