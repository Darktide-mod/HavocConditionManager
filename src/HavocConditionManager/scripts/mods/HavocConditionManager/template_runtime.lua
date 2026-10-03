local mod=get_mod("HavocConditionManager")
local S,R,A=mod.template_schema,mod.template_conditions,mod.template_registry
local Status=require("scripts/utilities/attack/player_unit_status")
local E={}
local owner,session,cache,prepared,gates,node_rules,contexts
local function weak() return setmetatable({},{__mode="k"}) end
function E.reset() owner=nil; session=nil; cache=weak(); prepared=weak(); gates=weak(); node_rules=weak(); contexts={} end
-- Retiring only EFL copies during a mission must preserve fine condition gates
-- and the prepared identity of templates already retained by native managers.
function E.invalidate() cache=weak() end
E.reset()
function E.config()
    local state=Managers.state or {}; local current=state.game_session or state.difficulty
    if not session or owner~=current then
        E.reset(); owner=current
        local director=get_mod("HavocEnemyDirector")
        local fine=director and director.is_gameplay_enabled and director.is_gameplay_enabled() and director.get_config and director.get_config()
        local coarse=director and director.active_coarse and director.active_coarse() or mod:get("native_configuration_v3")
        local Recycling=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/recycling_config")
        local recycling=director and director.active_recycling and director.active_recycling() or mod:get("recycling_v1")
        session={coarse=S.coarse_config(coarse),fine=A.validate_config(fine),recycling=Recycling.validate(recycling) or Recycling.validate()}
        session.changed=S.has_coarse_changes(session.coarse) or next(session.fine.patches)~=nil or next(session.fine.rules)~=nil
    end
    return session
end
function E.context(side)
    side=side or 1
    if not contexts[side] then contexts[side]=R.capture(Managers,Status,ScriptUnit,side) end
    return contexts[side]
end
function E.clear_context() contexts={} end
local function mark_changed(original,result,seen)
    if type(result)~="table" or original==result or seen[result] then return end
    seen[result]=true; prepared[result]=true
    for k,value in pairs(result) do if type(value)=="table" then mark_changed(type(original)=="table" and original[k],value,seen) end end
end
function E.prepare(root,family)
    if type(root)~="table" or not mod.has_local_gameplay_authority() then return root end
    local efl=mod.custom_efl
    local custom=efl and efl.session()
    local cfg=E.config()
    local entry=A.by_table[root]
    local source=not entry and A.children[root]
    local source_entry=entry or source and source.entry
    if not cfg.changed and (not custom or not source_entry or not efl.rules.targets[source_entry.id]) or prepared[root] then return root end
    if cache[root] then return cache[root] end
    if not entry then
        if source and #source.path>0 then
            local parent=E.prepare(source.entry.root,source.entry.family)
            local child=S.get(parent,source.path)
            cache[root]=child or root; return child or root
        end
    end
    family=entry and entry.family or family
    if not family then return root end
    local patch=entry and cfg.fine.patches[entry.id]
    local result=cfg.changed and S.apply(root,family,cfg.coarse,patch,A.breeds,A.by_table) or root
    local rules=entry and cfg.fine.rules[entry.id]
    if rules then
        for _,target in ipairs(entry.targets) do
            local rule=rules[target.id]
            if rule and #rule.clauses>0 then
                if result==root then result={}; for k,v in pairs(root) do result[k]=v end end
                if target.path then
                    S.set(result,target.path,R.compile(rule,S.get(result,target.path),E.context))
                elseif target.node then
                    S.set(result,{target.node},result[target.node]); node_rules[result[target.node]]=rule
                else gates[result]=rule end
            end
        end
    end
    if custom then
        local before=result
        result=efl.prepare(root,result,entry)
        if gates[before] then gates[result]=gates[before] end
    end
    mark_changed(root,result,{})
    cache[root]=result
    return result
end
function E.allowed(root,side)
    local rule=gates[root]
    return not rule or R.evaluate(rule,E.context(side))
end
function E.node_allowed(node)
    local rule=node_rules[node]
    return not rule or R.evaluate(rule,E.context(1))
end
function E.has_gate(root) return gates[root]~=nil end
return E
