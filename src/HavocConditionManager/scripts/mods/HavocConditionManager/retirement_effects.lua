-- Non-death retirement only suppresses the rotten-armour death payload.
-- Normal buff cleanup and real deaths retain the native callbacks.
local mod=get_mod("HavocConditionManager")
local Templates=require("scripts/settings/buff/buff_templates")
local retiring=setmetatable({},{__mode="k"})
mod.retiring_units=retiring
local rotten=Templates.mutator_rotten_armor
if rotten and rotten.stop_func then
    mod:hook(rotten,"stop_func",function(fn,data,context,...)
        if context and context.is_server and retiring[context.unit] then return end
        return fn(data,context,...)
    end)
end
return true
