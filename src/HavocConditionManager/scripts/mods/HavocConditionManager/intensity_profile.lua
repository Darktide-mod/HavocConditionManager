-- Strength is a coordinated profile, not a second multiplier at runtime.
local S=get_mod("HavocConditionManager").template_schema
local P={min=1,max=10,step=1}
-- Values at strength 1, 5 and 10. Unlisted controls stay at the baseline.
P.anchors={
    elite_density={1,1.75,3},
    roamer_population={1,1.2,1.5},
    encampments={1,1.1,1.25},
    patrols={1,3,6},
    horde_size={1,1.1,1.25},
    horde_frequency={1,1.08,1.2},
    horde_waves={1,1,1},
    coordinated_allowance={1,2,3},
    coordinated_load={1,2,3},
    trickle_size={1,1.1,1.25},
    trickle_frequency={1,1.05,1.1},
    special_slots={1,2,3},
    special_frequency={1,2,3.25},
    special_surges={1,3,6},
    monster_encounters={1,4,8},
    event_budget={1,1.1,1.25},
    combat_tolerance={1,1.5,2},
    recovery_duration={1,0.85,0.7},
}
local profiles={}
for level=1,10 do
    local values={}
    local segment=level<=5 and 1 or 2
    local alpha=level<=5 and (level-1)/4 or (level-5)/5
    for id,points in pairs(P.anchors) do
        values[id]=math.floor((points[segment]+(points[segment+1]-points[segment])*alpha)*100+0.5)/100
    end
    profiles[level]=S.coarse_config(values)
end
function P.values(level)
    if not S.finite(level) or level%1~=0 or not profiles[level] then return nil end
    return S.copy(profiles[level])
end
function P.match(values)
    for level=1,10 do
        local same=true
        for _,d in ipairs(S.coarse) do if math.abs(values[d.id]-profiles[level][d.id])>0.000001 then same=false;break end end
        if same then return level end
    end
end
local legacy_anchors={
    elite_density={1,1.75,3},
    roamer_population={1,0.95,0.85},
    encampments={1,1,1},
    patrols={1,3,6},
    horde_size={1,0.85,0.65},
    horde_frequency={1,1.15,1.35},
    horde_waves={1,1.5,2},
    coordinated_allowance={1,2,3},
    trickle_size={1,0.85,0.65},
    trickle_frequency={1,1,1},
    special_slots={1,2,3},
    special_frequency={1,2,3.25},
    special_surges={1,3,6},
    monster_encounters={1,4,8},
    event_budget={1,1,1},
    combat_tolerance={1,1.5,2},
    recovery_duration={1,0.85,0.7},
}
-- Only complete, exact old presets migrate. Individual custom controls survive.
function P.migrate(raw)
    if type(raw)~="table" or raw.coordinated_load~=nil then return end
    for level=1,10 do
        local segment=level<=5 and 1 or 2
        local alpha=level<=5 and (level-1)/4 or (level-5)/5
        local same=true
        for _,d in ipairs(S.coarse) do
            if d.id~="coordinated_load" then
                local p=legacy_anchors[d.id]
                local expected=p and math.floor((p[segment]+(p[segment+1]-p[segment])*alpha)*100+0.5)/100 or 1
                if not S.finite(raw[d.id]) or math.abs(raw[d.id]-expected)>0.000001 then same=false;break end
            end
        end
        if same then return P.values(level),level end
    end
end
return P
