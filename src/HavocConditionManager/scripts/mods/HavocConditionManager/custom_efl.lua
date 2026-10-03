-- III/IV are HCM balance choices, derived from native I/II pacing anchors.
-- Their UI IDs never enter native circumstance tables or mission data.
local R={storage_key="hcm_custom_efl_v1",mode_key="hcm_custom_efl_modes_v1",
    native_i="mutator_increased_difficulty",native_ii="mutator_highest_difficulty"}
R.choices={[1]=R.native_i,[2]=R.native_ii,[3]="hcm_efl_3",[4]="hcm_efl_4"}
R.targets={["mutators/havoc_mutator_more_captains_02"]=true,["mutators/havoc_mutator_monster_specials_02"]=true,["hordes/mutator_horde/havoc_02"]=true}
function R.valid_tier(t) return type(t)=="number" and t==t and t%1==0 and t>=1 and t<=4 end
function R.tier(choice)
    for tier,id in ipairs(R.choices) do if choice==id then return tier end end
end
function R.record(tier)
    if not R.valid_tier(tier) or tier<3 then return end
    return {version=1,tier=tier,native_id=R.native_ii}
end
function R.validate_record(v)
    if type(v)~="table" or getmetatable(v) or v.version~=1 or not R.valid_tier(v.tier) or v.tier<3 or v.native_id~=R.native_ii then return end
    for key in pairs(v) do if key~="version" and key~="tier" and key~="native_id" then return end end
    return R.record(v.tier)
end
function R.validate_modes(v)
    if v==nil then return {} end
    if type(v)~="table" or getmetatable(v) then return end
    local clean={}
    for key,value in pairs(v) do
        if key~="hcm" and key~="hed" then return end
        clean[key]=R.validate_record(value);if not clean[key] then return end
    end
    return clean
end
function R.native_ii_only(parsed)
    if type(parsed)~="table" or type(parsed.circumstances)~="table" then return false end
    local count=0
    for _,id in ipairs(parsed.circumstances) do
        if id==R.native_i or id==R.choices[3] or id==R.choices[4] then return false end
        if id==R.native_ii then count=count+1 end
    end
    return count==1
end
function R.extend(value,i,ii,tier)
    assert(R.valid_tier(tier) and tier>=3,"Invalid custom EFL tier")
    assert(type(i)=="number" and i>0 and i<math.huge and type(ii)=="number" and ii>0 and ii<math.huge,"Invalid native EFL pacing anchors")
    return value*(ii/i)^(tier-2)
end
local function copy(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
local function range(value,i,ii,tier)
    return {R.extend(value[1],i[1],ii[1],tier),R.extend(value[2],i[2],ii[2],tier)}
end
-- Return a private root and an ownership-limited restoration callback. Other
-- settings retain the existing coarse/fine compiler's values and references.
function R.prepare(original,prepared,entry,registry,tier)
    if not R.valid_tier(tier) or tier<3 or not entry then return prepared end
    local id=entry.id
    if not R.targets[id] then return prepared end
    local out=copy(prepared)
    if id=="mutators/havoc_mutator_more_captains_02" then
        local i=registry.by_id["mutators/havoc_mutator_more_captains_01"].root.modify_pacing
        local ii=original.modify_pacing
        out.modify_pacing=copy(prepared.modify_pacing)
        local baseline=prepared.modify_pacing.monsters_per_travel_distance
        local custom=range(baseline,i.monsters_per_travel_distance,ii.monsters_per_travel_distance,tier)
        out.modify_pacing.monsters_per_travel_distance=custom
        return out,function() if out.modify_pacing.monsters_per_travel_distance==custom then out.modify_pacing.monsters_per_travel_distance=baseline end end
    elseif id=="mutators/havoc_mutator_monster_specials_02" then
        local i=registry.by_id["mutators/havoc_mutator_monster_specials_01"].root.init_modify_pacing.specials_monster_spawn_config
        local ii=original.init_modify_pacing.specials_monster_spawn_config
        out.init_modify_pacing=copy(prepared.init_modify_pacing)
        local baseline=prepared.init_modify_pacing.specials_monster_spawn_config
        local custom=copy(baseline)
        local chance=math.min(1,R.extend(baseline.chance_to_spawn_monster,i.chance_to_spawn_monster,ii.chance_to_spawn_monster,tier))
        local duration=range(baseline.max_monster_duration,i.max_monster_duration,ii.max_monster_duration,tier)
        custom.chance_to_spawn_monster=chance
        custom.max_monster_duration=duration
        out.init_modify_pacing.specials_monster_spawn_config=custom
        return out,function()
            -- Native SpecialsPacing retains this child directly. Restore it too.
            if custom.chance_to_spawn_monster==chance then custom.chance_to_spawn_monster=baseline.chance_to_spawn_monster end
            if custom.max_monster_duration==duration then custom.max_monster_duration=baseline.max_monster_duration end
        end
    elseif id=="hordes/mutator_horde/havoc_02" then
        local i=registry.by_id["hordes/mutator_horde/havoc_01"].root
        local baseline=prepared.horde_timer_range
        local custom=range(baseline,i.horde_timer_range,original.horde_timer_range,tier)
        out.horde_timer_range=custom
        return out,function() if out.horde_timer_range==custom then out.horde_timer_range=baseline end end
    end
    return prepared
end
return R
