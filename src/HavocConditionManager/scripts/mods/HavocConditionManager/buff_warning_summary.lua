-- Summarize this one repeated warning; the native 300-entry Buff pool and
-- overflow rejection are untouched. Encounter placement separately defers its
-- provisional section warning until the final location plan is known.
local mod=get_mod("HavocConditionManager")
local E=mod.template_runtime
local Pacing=require("scripts/managers/pacing/pacing_manager")
local pending,owner,deadline,emit=0,nil,nil,nil
local function flush()
    if pending>0 then
        emit("BuffExtensionBase","Out of proc event tables: %d additional events rejected by native capacity (repeated warnings summarized).",pending)
        pending=0
    end
end
mod.finish_native_warning_summary=function()
    flush();owner=nil;deadline=nil;emit=nil
end
mod.update_native_warning_summary=function(t)
    if pending>0 and deadline and t>=deadline then flush();deadline=t+1 end
end
if Log and Log.warning then
    mod:hook(Log,"warning",function(fn,tag,message,...)
        if mod.defer_native_encounter_warning and mod.defer_native_encounter_warning(fn,tag,message,...) then return end
        if tag~="BuffExtensionBase" or message~="Out of proc event tables, ignoring proc!" or not mod.has_local_gameplay_authority() or not E.config().changed then
            return fn(tag,message,...)
        end
        local current=Managers.state.game_session or Managers.state.difficulty
        local t=Managers.time and Managers.time:time("gameplay")
        if not t then return fn(tag,message,...) end
        if owner~=current or not deadline then
            flush();owner=current;deadline=t+1;emit=fn
            return fn(tag,message,...)
        end
        pending=pending+1
        if t>=deadline then flush();deadline=t+1 end
    end)
    mod:hook_safe(Pacing,"destroy",mod.finish_native_warning_summary)
end
return true
