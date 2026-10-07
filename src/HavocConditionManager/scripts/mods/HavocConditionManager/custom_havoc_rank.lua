-- HCM-owned 41-60 extension. Native modifier IDs, tiers and rank tables stay intact.
local Settings=require("scripts/settings/havoc_settings")
local Config=require("scripts/settings/havoc/havoc_modifier_config")
local BuffTemplates=require("scripts/settings/buff/buff_templates")
local R={max=60,native_max=40,storage_key="hcm_custom_havoc_v1"}
-- Extend selected definitions only. Fractions remain fractions until native
-- consumers quantize actual counts (special slots use ceil; roamer limits ceil).
local fields={
    buff_elites={modify_elite_health=true},
    buff_specials={modify_special_health=true},
    buff_monsters={add_num_monsters=true,modify_monster_health=true},
    buff_horde={modify_horde_health=true,modify_horde_hit_mass=true},
    more_alive_specials={add_max_alive_specials=true},
    more_elites={add_more_elites=true},more_ogryns={add_more_ogryns=true},
    ammo_pickup_modifier={ammo_pickup_modifier=true},
    horde_spawn_rate_increase={horde_spawn_rate_modifier=true},
    terror_event_point_increase={terror_event_point_modifier=true},
    melee_minion_power_level_buff={melee_minion_power_level_modifier=true},
    melee_minion_attack_speed={melee_attack_speed=true},
    ranged_minion_attack_speed={ranged_attack_speed=true,minion_num_shots_modifier=true},
    melee_minion_permanent_damage={permanent_damage_ratio=true},
    reduce_health_and_wounds={max_health_modifier=true},
    reduce_toughness={toughness=true},
    reduce_toughness_regen={toughness_regen_rate_modifier=true},
    havoc_vent_speed_reduction={vent_warp_charge_speed=true},
}
local function copy(t)
    local result={}
    for k,v in pairs(t) do result[k]=type(v)=="table" and copy(v) or v end
    return result
end
function R.validate(rank)
    return type(rank)=="number" and rank==rank and rank>=1 and rank<=R.max and rank%1==0
end
function R.validate_record(value)
    if type(value)~="table" or getmetatable(value)~=nil then return end
    for k in pairs(value) do if k~="version" and k~="requested_rank" and k~="native_rank" then return end end
    if value.version~=1 or not R.validate(value.requested_rank) or value.native_rank~=math.min(value.requested_rank,R.native_max) then return end
    return {version=1,requested_rank=value.requested_rank,native_rank=value.native_rank}
end
function R.record(rank)
    assert(R.validate(rank),"Custom Havoc rank must be a finite integer from 1 to 60")
    return {version=1,requested_rank=rank,native_rank=math.min(rank,R.native_max)}
end
local function modifier_names()
    local names={}
    for name in pairs(Settings.modifier_templates) do names[name]=true end
    for name in pairs(Settings.positive_modifier_templates) do names[name]=true end
    return names
end
function R.preset(rank,get)
    local result=R.record(rank)
    result.modifiers={}
    for name in pairs(modifier_names()) do result.modifiers[name]=get("havoc_modifier_"..name) or 0 end
    result.customizable=get("havoc_modifiers_customizable")==true
    return R.validate_preset(result)
end
function R.validate_preset(value)
    if type(value)~="table" or getmetatable(value)~=nil then return end
    local allowed={version=true,requested_rank=true,native_rank=true,modifiers=true,customizable=true}
    for key in pairs(value) do if not allowed[key] then return end end
    local result=R.validate_record({version=value.version,requested_rank=value.requested_rank,native_rank=value.native_rank})
    if not result or type(value.customizable)~="boolean" or type(value.modifiers)~="table" or getmetatable(value.modifiers)~=nil then return end
    local names=modifier_names();local selected={}
    for name,level in pairs(value.modifiers) do
        local templates=Settings.modifier_templates[name] or Settings.positive_modifier_templates[name]
        if not names[name] or type(level)~="number" or level~=level or level%1~=0 or level<0 or (level>0 and not templates[level]) then return end
        selected[name]=level;names[name]=nil
    end
    if next(names)~=nil then return end
    result.modifiers=selected;result.customizable=value.customizable
    return result
end
function R.selection_state(get)
    local result={}
    for name in pairs(modifier_names()) do result[#result+1]={key="havoc_modifier_"..name,value=get("havoc_modifier_"..name)} end
    result[#result+1]={key="havoc_modifiers_customizable",value=get("havoc_modifiers_customizable")}
    return result
end
function R.validate_modes(value)
    if value==nil then return {} end
    if type(value)~="table" or getmetatable(value)~=nil then return end
    local result={}
    for mode,preset in pairs(value) do
        if mode~="hcm" and mode~="hed" then return end
        local checked=R.validate_preset(preset)
        if not checked then return end
        result[mode]=checked
    end
    return result
end
function R.generate(fn,rank,...)
    assert(R.validate(rank),"Custom Havoc rank must be a finite integer from 1 to 60")
    return fn(math.min(rank,R.native_max),...)
end
local function values(definition,allowed)
    local result,buff_name={}
    for key,value in pairs(definition) do
        if allowed[key] and type(value)=="number" then result[key]=value
        elseif type(value)=="string" and BuffTemplates[value] then
            buff_name=value
            for stat,amount in pairs(BuffTemplates[value].stat_buffs or {}) do
                if allowed[stat] then result[stat]=amount end
            end
        end
    end
    return result,buff_name
end
local curves
local function native_curves()
    if curves then return curves end
    assert(#Config==40,"Re-audit the native Havoc rank table before extending a changed source version")
    local result={}
    for name,allowed in pairs(fields) do
        local arrivals={};local previous
        for rank=1,R.native_max do
            local tier=Config[rank][name]
            if tier and tier~=previous then arrivals[#arrivals+1]={rank=rank,tier=tier};previous=tier end
        end
        local last,before=arrivals[#arrivals],arrivals[#arrivals-1]
        assert(before and last,"Missing audited modifier attainments: "..name)
        local templates=Settings.modifier_templates[name]
        local a=values(templates[before.tier],allowed)
        local b=values(templates[last.tier],allowed)
        local slope={}
        for key in pairs(allowed) do
            assert(type(a[key])=="number" and type(b[key])=="number","Missing audited numeric modifier field: "..name.."/"..key)
            slope[key]=(b[key]-a[key])/(last.rank-before.rank)
        end
        result[name]={slope=slope,previous_rank=before.rank,last_rank=last.rank}
    end
    curves=result
    return curves
end
function R.capture(rank,selected)
    local record=R.record(rank)
    if rank<=R.native_max then return end
    local result={record=record,modifiers={},scalar_deltas={},buff_values={}}
    local seen={}
    for _,choice in ipairs(selected or {}) do
        local name,level=choice.name,choice.level
        local templates=Settings.modifier_templates[name] or Settings.positive_modifier_templates[name]
        assert(type(level)=="number" and level%1==0 and level>0 and templates and templates[level],"Invalid selected Havoc modifier: "..tostring(name))
        assert(not seen[name],"Duplicate selected Havoc modifier: "..name)
        seen[name]=true;result.modifiers[#result.modifiers+1]={name=name,level=level}
        if fields[name] then
            local current,buff_name=values(templates[level],fields[name])
            local curve=native_curves()[name]
            local extended={}
            for key,amount in pairs(current) do
                local delta=(rank-R.native_max)*curve.slope[key]
                extended[key]=amount+delta
                if not buff_name then result.scalar_deltas[key]=delta end
            end
            if buff_name then result.buff_values[buff_name]=extended end
        end
    end
    return result
end
function R.same_modifiers(a,b)
    if type(a)~="table" or type(b)~="table" or #a~=#b then return false end
    local lookup={}
    for _,choice in ipairs(a) do if lookup[choice.name] then return false end;lookup[choice.name]=choice.level end
    for _,choice in ipairs(b) do if lookup[choice.name]~=choice.level then return false end;lookup[choice.name]=nil end
    return next(lookup)==nil
end
function R.apply_scalars(snapshot,instance)
    for key,delta in pairs(snapshot.scalar_deltas) do
        assert(type(instance[key])=="number","Missing native selected modifier field: "..key)
        instance[key]=instance[key]+delta
    end
end
function R.prepare_buff(snapshot,template,cache)
    local overrides=template and snapshot.buff_values[template.name]
    if not overrides then return template end
    if cache[template] then return cache[template] end
    local result={};for key,value in pairs(template) do result[key]=value end
    result.stat_buffs={};for key,value in pairs(template.stat_buffs) do result.stat_buffs[key]=value end
    for key,value in pairs(overrides) do result.stat_buffs[key]=value end
    cache[template]=result
    return result
end
R.copy=copy
return R
