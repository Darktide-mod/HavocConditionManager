-- Supported native tactics have stage, capable-player and load predicates.
-- Replace only the known upper-load predicate; retain every other condition.
local M={}
local supported={coordinated_special_attack=true,elite_coordinated_special_attack=true,
    elite_roamer_mix_vector=true,elite_sandwich_waves=true,sandwich=true,ranged_push_from_behind=true}
function M.apply(root,family,cfg,set,boundaries)
    if family~="hordes" or (cfg.coordinated_load or 1)==1 then return 0 end
    local count=0
    for name,tactic in pairs(root.coordinated_horde_strike_settings or {}) do
        local original=tactic.conditions
        if supported[name] and type(original)=="table" and #original==3
            and type(original[1])=="function" and type(original[2])=="function" and type(original[3])=="function" then
            local maximum=35*cfg.coordinated_load
            local medium=name=="ranged_push_from_behind"
            local conditions={}
            for i=1,3 do
                local index,native=i,original[i]
                conditions[i]=function(side)
                    if index~=3 then return native(side) end
                    local pacing=Managers.state.pacing
                    local load=pacing:total_challenge_rating()
                    return load<maximum and (not medium or load>=8)
                end
            end
            set({"coordinated_horde_strike_settings",name,"conditions"},conditions)
            count=count+1
        end
    end
    return count
end
return M
