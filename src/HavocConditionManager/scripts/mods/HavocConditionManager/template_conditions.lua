-- Named, data-only rules using the same game state as native pacing predicates.
-- Configuration contains identifiers and values, never Lua source or functions.
local R={definitions={},order={}}
local function define(id,en,cn,kind,min,max,default,options)
    local d={id=id,en=en,cn=cn,kind=kind or "none",min=min,max=max,default=default,options=options}
    R.definitions[id]=d; R.order[#R.order+1]=d
end
define("always","No additional requirement","无额外要求")
define("players_min","At least this many capable players","有效玩家人数至少为","number",1,4,2)
define("players_max","At most this many capable players","有效玩家人数至多为","number",1,4,4)
define("stage","Pacing stage is","战斗节奏处于","choice",nil,nil,"build_up_tension",{"build_up_tension_low","build_up_tension","build_up_tension_high","sustain_tension_peak","tension_peak_fade","relax"})
define("building","Any build-up stage","任一升压阶段")
define("load_min","Combat load is at least","当前战斗负担至少为","number",0,2000,35)
define("load_max","Combat load is at most","当前战斗负担至多为","number",0,2000,35)
define("monster_active","A monster is engaged","有怪物正在交战")
define("monster_idle","No monster is engaged","没有怪物正在交战")
define("event_active","A mission event is active","任务事件正在进行")
define("event_idle","No mission event is active","没有任务事件正在进行")
define("horde_active","A horde is active","有尸潮正在进行")
define("horde_idle","No horde is active","没有尸潮正在进行")
define("low_coherency","At least one player has low coherency","至少一名玩家的协同人数不超过二")
define("progress_min","Main-path progress is at least","主路径推进距离至少为","number",0,10000,100)
define("progress_max","Main-path progress is at most","主路径推进距离至多为","number",0,10000,1000)
define("stationary","No forward progress for this long","未继续向前推进达到","number",1,600,30)
define("low_stage_time","Low-pressure period lasts this long","低压阶段持续达到","number",1,600,50)
define("combat_vector_min","Engaged ranged formations at least","正在交战的射击阵位敌人数至少为","number",0,300,9)
define("affix_active","DIY affix is active (paste ID)","DIY 词条已启用（粘贴 ID）","text",nil,nil,"example")
define("signal_active","DIY signal is active (paste name)","DIY 信号生效中（粘贴名称）","text",nil,nil,"example")

local function finite(v) return type(v)=="number" and v==v and v~=math.huge and v~=-math.huge end
function R.validate(rule)
    if type(rule)~="table" or getmetatable(rule) then return false,"rule" end
    for key in pairs(rule) do if key~="mode" and key~="match" and key~="clauses" then return false,"rule field" end end
    if rule.mode~="append" and rule.mode~="replace" then return false,"rule mode" end
    if rule.match~="all" and rule.match~="any" then return false,"rule match" end
    if type(rule.clauses)~="table" or #rule.clauses>8 then return false,"rule clauses" end
    local count=0
    for key,clause in pairs(rule.clauses) do
        count=count+1
        if type(key)~="number" or key%1~=0 or key<1 or key>#rule.clauses or type(clause)~="table" then return false,"rule clause" end
        for field in pairs(clause) do if field~="condition" and field~="value" then return false,"clause field" end end
        local d=R.definitions[clause.condition]
        if not d then return false,"condition" end
        if d.kind=="number" and (not finite(clause.value) or clause.value<d.min or clause.value>d.max or clause.value%1~=0) then return false,"condition value" end
        if d.kind=="choice" then
            local found=false; for _,option in ipairs(d.options) do if option==clause.value then found=true; break end end
            if not found then return false,"condition option" end
        end
        if d.kind=="none" and clause.value~=nil then return false,"unexpected condition value" end
        if d.kind=="text" and (type(clause.value)~="string" or #clause.value>64 or not clause.value:match("^[%w_%-]+$")) then return false,"condition identifier" end
    end
    return count==#rule.clauses
end
function R.default_clause(id)
    local d=R.definitions[id] or R.definitions.always
    return {condition=d.id,value=d.default}
end
local evaluators={
    always=function() return true end,
    affix_active=function(c,v) return c.affix~=nil and c.affix[v]==true end,
    signal_active=function(c,v) return c.signal~=nil and c.signal[v]==true end,
    players_min=function(c,v) return c.players~=nil and c.players>=v end,
    players_max=function(c,v) return c.players~=nil and c.players<=v end,
    stage=function(c,v) return c.stage==v end,
    building=function(c) return c.stage=="build_up_tension_low" or c.stage=="build_up_tension" or c.stage=="build_up_tension_high" end,
    load_min=function(c,v) return c.load~=nil and c.load>=v end,
    load_max=function(c,v) return c.load~=nil and c.load<=v end,
    monster_active=function(c) return c.monsters~=nil and c.monsters>0 end,
    monster_idle=function(c) return c.monsters==0 end,
    event_active=function(c) return c.events~=nil and c.events>0 end,
    event_idle=function(c) return c.events==0 end,
    horde_active=function(c) return c.hordes~=nil and c.hordes>0 end,
    horde_idle=function(c) return c.hordes==0 end,
    low_coherency=function(c) return c.low_coherency==true end,
    progress_min=function(c,v) return c.progress~=nil and c.progress>=v end,
    progress_max=function(c,v) return c.progress~=nil and c.progress<=v end,
    stationary=function(c,v) return c.stationary~=nil and c.stationary>=v end,
    low_stage_time=function(c,v) return (c.stage=="build_up_tension_low" or c.stage=="build_up_tension") and c.low_stage_time~=nil and c.low_stage_time>=v end,
    combat_vector_min=function(c,v) return c.combat_vector~=nil and c.combat_vector>=v end,
}
function R.evaluate(rule,context)
    if not rule or #rule.clauses==0 then return true end
    local all=rule.match~="any"
    for _,clause in ipairs(rule.clauses) do
        local evaluate=evaluators[clause.condition]
        local passed=evaluate and evaluate(context,clause.value) or false
        if all and not passed then return false end
        if not all and passed then return true end
    end
    return all
end
function R.compile(rule,original,context_provider)
    if not rule or #rule.clauses==0 then return original end
    local result={}
    if rule.mode=="append" then for _,fn in ipairs(original or {}) do result[#result+1]=fn end end
    result[#result+1]=function(target_side_id) return R.evaluate(rule,context_provider(target_side_id)) end
    return result
end
function R.capture(managers,status,script_unit,target_side_id)
    local state=managers and managers.state or {}; local pacing=state.pacing; local c={}
    if pacing then
        if pacing.state then c.stage=pacing:state() end
        if pacing.total_challenge_rating then c.load=pacing:total_challenge_rating() end
        if pacing.num_aggroed_monsters then c.monsters=pacing:num_aggroed_monsters() end
        if pacing.get_mission_progression then c.progress=pacing:get_mission_progression() end
        if pacing.low_state_duration then c.low_stage_time=pacing:low_state_duration() end
        c.stationary=pacing._time_since_forward_mission_progressed
    end
    if state.terror_event and state.terror_event.num_active_events then c.events=state.terror_event:num_active_events() end
    if state.horde and state.horde.num_active_hordes then c.hordes=state.horde:num_active_hordes() end
    local extensions=state.extension
    if extensions and extensions.system then
        local side_system=extensions:system("side_system")
        local side=side_system and side_system:get_side(target_side_id or 1)
        if side and side.valid_player_units and script_unit then
            c.players=0; c.low_coherency=false
            for _,unit in ipairs(side.valid_player_units) do
                local data=script_unit.has_extension and script_unit.has_extension(unit,"unit_data_system") or script_unit.extension and script_unit.extension(unit,"unit_data_system")
                local component=data and data:read_component("character_state")
                if component and status and status.requires_help and not status.requires_help(component) then c.players=c.players+1 end
                local coherency=script_unit.has_extension and script_unit.has_extension(unit,"coherency_system")
                if coherency then
                    local n=coherency:num_units_in_coherency()
                    if n and n<=2 then c.low_coherency=true end
                end
            end
        end
        local vector=extensions:system("combat_vector_system")
        if vector and vector.num_aggroed_combat_vector_minions then c.combat_vector=vector:num_aggroed_combat_vector_minions() end
    end
    local hcm=get_mod and get_mod("HavocConditionManager")
    if hcm and hcm.diy_api then hcm.diy_api.context(c) end
    return c
end
return R
