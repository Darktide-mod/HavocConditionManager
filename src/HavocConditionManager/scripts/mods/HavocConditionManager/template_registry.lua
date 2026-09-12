local mod=get_mod("HavocConditionManager")
local S=mod.template_schema
local A={entries={},by_id={},by_table=setmetatable({},{__mode="k"})}
local discovering=true
A.breeds=require("scripts/settings/breed/breeds")
local function sorted(t)
    local keys={} for k in pairs(t) do keys[#keys+1]=k end
    table.sort(keys,function(a,b) return tostring(a)<tostring(b) end); return keys
end
function A.add(id,family,root,level)
    if type(root)~="table" or A.by_id[id] then return end
    local entry={id=id,family=family,root=root,level=level,items={},fields={},targets={}}
    A.entries[#A.entries+1]=entry; A.by_id[id]=entry
    if not A.by_table[root] then A.by_table[root]=entry end
    local tactics=root.coordinated_horde_strike_settings
    for _,key in ipairs(sorted(tactics or {})) do
        for _,slot in ipairs({"conditions","high_chance_conditions"}) do
            if type(tactics[key][slot])=="table" then
                local path={"coordinated_horde_strike_settings",key,slot}
                entry.targets[#entry.targets+1]={id=S.path_key(path),path=path,replace=true}
            end
        end
    end
    if family=="specials" or family=="events" or family=="hordes" or family=="monsters" or family=="roamers" then
        entry.targets[#entry.targets+1]={id="encounter",replace=false}
    elseif family=="mission_events" then
        for i,node in ipairs(root) do
            if type(node)=="table" and node[1]=="spawn_by_points" and not node.mission_objective_id then
                entry.targets[#entry.targets+1]={id=tostring(i).."/start",node=i,replace=false}
            end
        end
    end
    -- Runtime test/custom native entries can also be added after discovery.
    if not discovering then entry.items,entry.fields=S.describe(root,family,A.breeds,A.by_table) end
    return entry
end
local modules={
    {"pacing","scripts/managers/pacing/pacing_templates"},
    {"roamers","scripts/managers/pacing/roamer_pacing/roamer_pacing_templates"},
    {"hordes","scripts/managers/pacing/horde_pacing/horde_pacing_templates","resistance_templates"},
    {"specials","scripts/managers/pacing/specials_pacing/specials_pacing_templates","resistance_templates"},
    {"monsters","scripts/managers/pacing/monster_pacing/monster_pacing_templates","challenge_templates"},
    {"events","scripts/managers/pacing/auto_event/templates/auto_event_templates"},
    {"mutators","scripts/settings/mutator/mutator_templates"},
}
for _,data in ipairs(modules) do
    local templates=require(data[2])
    for _,name in ipairs(sorted(templates)) do
        local root=templates[name]
        if type(root)=="table" then
            if data[3] then
                for _,level in ipairs(sorted(root[data[3]] or {})) do A.add(data[1].."/"..name.."/"..level,data[1],root[data[3]][level],level) end
            else A.add(data[1].."/"..name,data[1],root) end
        end
    end
end
local event_templates=require("scripts/settings/terror_event/terror_event_templates")
for _,file in ipairs(sorted(event_templates)) do
    local template=event_templates[file]
    for _,name in ipairs(sorted(template.events or {})) do A.add("mission_events/"..file.."/"..name,"mission_events",template.events[name]) end
end
table.sort(A.entries,function(a,b) return a.id<b.id end)
discovering=false
-- Shared registered child templates have their own editor and compiler hook.
-- Stop at those boundaries so one native source cannot be scaled twice.
for _,entry in ipairs(A.entries) do entry.items,entry.fields=S.describe(entry.root,entry.family,A.breeds,A.by_table) end
-- Child templates passed independently by a native mutator retain their source
-- path. They are described in their original parent's editor.
A.children=setmetatable({},{__mode="k"})
local function index(value,entry,path,seen)
    if type(value)~="table" or seen[value] or A.children[value] then return end; seen[value]=true
    A.children[value]={entry=entry,path=path}
    for k,v in pairs(value) do if type(k)=="number" or type(k)=="string" then index(v,entry,S.append(path,k),seen) end end
end
for _,entry in ipairs(A.entries) do index(entry.root,entry,{}, {}) end
function A.validate_config(raw)
    local clean={version=2,patches={},rules={},seed=nil}; local rejected={}
    if type(raw)~="table" then return clean,rejected end
    if S.finite(raw.seed) and raw.seed%1==0 and raw.seed>=1 and raw.seed<=2147483646 then clean.seed=raw.seed end
    for id,patch in pairs(type(raw.patches)=="table" and raw.patches or {}) do
        local entry=A.by_id[id]
        if entry and type(patch)=="table" then
            local values={}
            for key,value in pairs(patch) do
                local item=entry.fields[key]
                if item and S.validate_value(item,value,A.breeds) then values[key]=S.copy(value) else rejected[#rejected+1]=id.."/"..tostring(key) end
            end
            if next(values) then
                local valid,why=A.validate_patch(entry,values)
                if valid then clean.patches[id]=values else rejected[#rejected+1]=id.."/"..why end
            end
        else rejected[#rejected+1]=tostring(id) end
    end
    for id,rules in pairs(type(raw.rules)=="table" and raw.rules or {}) do
        local entry=A.by_id[id]; local available={}
        if entry then for _,target in ipairs(entry.targets) do available[target.id]=target end end
        for key,rule in pairs(type(rules)=="table" and rules or {}) do
            local target=available[key]
            if target and mod.template_conditions.validate(rule) and (rule.mode=="append" or target.replace) then
                clean.rules[id]=clean.rules[id] or {}; clean.rules[id][key]=S.copy(rule)
            else rejected[#rejected+1]=tostring(id).."/"..tostring(key) end
        end
    end
    return clean,rejected
end
function A.validate_patch(entry,patch)
    local result=S.apply(entry.root,entry.family,S.coarse_config(),patch,A.breeds,A.by_table)
    local checked,auto_compositions={},{}
    for key in pairs(patch) do
        local item=entry.fields[key]
        if item and entry.family=="events" and item.definition.key=="weights" and item.path[1]=="composition" then
            auto_compositions[item.path[2]]=true
        elseif item and (item.definition.key=="weight" or item.definition.key=="weights") then
            local path=S.copy(item.path); table.remove(path)
            if item.definition.key=="weight" then table.remove(path) end
            local id=S.path_key(path)
            if not checked[id] then
                checked[id]=true; local total=0; local parent=S.get(result,path)
                if type(parent)=="table" then
                    for _,v in pairs(parent) do
                        if type(v)=="number" then total=total+v
                        elseif type(v)=="table" and type(v.weight)=="number" then total=total+v.weight end
                    end
                    if total<=0 then return false,"weights must include a positive value" end
                end
            end
        end
    end
    for name in pairs(auto_compositions) do
        local before=entry.root.composition[name].breeds
        local after=result.composition[name].breeds
        local cells={}
        for _,row in ipairs(before) do
            for difficulty,curve in pairs(row.weights or {}) do
                if type(curve)=="table" then for heat in pairs(curve) do cells[tostring(difficulty).."/"..tostring(heat)]={difficulty,heat} end
                elseif type(curve)=="number" then cells[tostring(difficulty)]={difficulty} end
            end
        end
        local function total(rows,cell)
            local sum=0
            for _,row in ipairs(rows) do
                local value=row.weights and row.weights[cell[1]]
                if cell[2] and type(value)=="table" then value=value[cell[2]] end
                if type(value)=="number" then sum=sum+value end
            end
            return sum
        end
        for _,cell in pairs(cells) do
            if total(before,cell)>0 and total(after,cell)<=0 then return false,"event composition must retain a positive weight at each difficulty and heat stage" end
        end
    end
    -- Specialist spawner bounds are separate native maps; preserve ordering.
    local near,far=result.spawners_min_range,result.spawners_max_range
    if type(near)=="table" and type(far)=="table" then
        for breed,n in pairs(near) do if type(n)=="number" and type(far[breed])=="number" and n>far[breed] then return false,"spawner distance order" end end
    end
    return true
end
return A
