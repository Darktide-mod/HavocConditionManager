-- Import SoloPlay's current selection catalog. No aliases or native definitions
-- are registered by HCM; the game and SoloPlay remain their only owners.
local mod=get_mod("HavocConditionManager")
local Templates=require("scripts/settings/circumstance/circumstance_templates")
local Mutators=require("scripts/settings/mutator/mutator_templates")
local C={labels={havoc=mod:localize("ui_021"),maelstrom=mod:localize("ui_022"),event=mod:localize("ui_023"),general=mod:localize("ui_049")}}
local categories={}
local difficulties={mutator_increased_difficulty=1,mutator_highest_difficulty=2}
local function available(id)
    local t=Templates[id]
    if not t or type(t.mutators)~="table" or difficulties[id] then return false end
    for _,name in ipairs(t.mutators) do if not Mutators[name] then return false end end
    return true
end
function C.category(id) return categories[id] end
function C.is_reference() return false end
function C.environment_available(settings,mission,id)
    if id=="default" then return true end
    local allowed=settings.lookup.theme_circumstances_of_havoc_missions
    return allowed and allowed[mission] and allowed[mission][id] and available(id) or false
end
function C.extend(settings)
    local ids,lookup,seen={},{},{}
    local native_havoc=settings.lookup.havoc_circumstances or {}
    for _,list in ipairs({settings.order.havoc_circumstances or {},settings.order.circumstances or {}}) do
        for _,id in ipairs(list) do
            local template=Templates[id]
            if not seen[id] and id~="default" and available(id) and (not template.theme_tag or template.theme_tag=="default") then
                seen[id]=true; lookup[id]=true; ids[#ids+1]=id
                if not categories[id] then
                    if native_havoc[id] then categories[id]="havoc"
                    elseif id:find("flash_mission",1,true) then categories[id]="maelstrom"
                    elseif id:find("event",1,true) or template.ui and template.ui.description and tostring(template.ui.description):find("event",1,true) then categories[id]="event"
                    else categories[id]="general" end
                end
                settings.loc.havoc_circumstances[id]=settings.loc.havoc_circumstances[id] or settings.loc.circumstances[id] or id
            end
        end
    end
    local order={havoc=1,maelstrom=2,event=3,general=4}
    table.sort(ids,function(a,b) return order[categories[a]]==order[categories[b]] and a<b or order[categories[a]]<order[categories[b]] end)
    settings.order.havoc_circumstances=ids; settings.lookup.havoc_circumstances=lookup
    return settings
end
function C.migrate_difficulty(selected,base)
    local best=base:get("havoc_difficulty_circumstance"); local rank=difficulties[best] or 0
    for _,id in ipairs(selected) do if (difficulties[id] or 0)>rank then best=id; rank=difficulties[id] end end
    if rank>0 and best~=base:get("havoc_difficulty_circumstance") then base:set("havoc_difficulty_circumstance",best) end
end
return C
