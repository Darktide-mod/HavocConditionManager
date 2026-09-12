-- Reader-facing descriptions shared by the main selector and package manager.
local D={}
local words={
    custom={"Custom","自定义","自訂"}, manager={"DIY manager","DIY 管理","DIY 管理"},
    loaded={"Loaded","已加载","已載入"}, unloaded={"Disabled","已停用","已停用"},
    havoc={"Havoc","浩劫","浩劫"}, maelstrom={"Maelstrom","金级","金級"}, event={"Events","活动","活動"}, diy={"DIY","DIY","DIY"}, all={"All","全部","全部"}, active={"Enabled","已启用","已啟用"},
    scroll_help={"Scroll to read more", "滚轮翻页查看完整说明", "滾輪翻頁查看完整說明"},
    extract={"Extract DIY templates","解压模板DIY词条","解壓模板DIY詞條"},
    extract_help={"Unpack the built-in templates into the DIY folder, replace matching folders, and reload the library. Templates stay hidden until extracted.","将内置模板解包到 DIY 目录，覆盖同名词条并立即加载。未解包的模板不会出现在词条列表中。","將內建模板解包到 DIY 目錄，覆蓋同名詞條並立即載入。未解包的模板不會出現在詞條清單中。"},
    manage_help={"Refresh to load edited or newly installed folders. Click a row to read its description. Select gameplay conditions on the main Conditions page.","刷新可加载新增或修改的词条包。点击列表查看说明；需要启用的词条请到主界面的「词条配置」中勾选。","重新整理可載入新增或修改的詞條套件。點擊清單查看說明；需要啟用的詞條請到主介面的「詞條配置」中勾選。"},
    enabled={"Custom effects enabled","自定义效果已开启","自訂效果已開啟"},
    disabled={"Custom effects disabled","自定义效果已关闭","自訂效果已關閉"},
    master_help={"Selected custom conditions apply next mission while this switch is on. Turning it off keeps your selections.","开启后，勾选的自定义词条在下一局生效。关闭时保留勾选，但不应用效果。","開啟後，勾選的自訂詞條在下一局生效。關閉時保留勾選，但不套用效果。"},
    selected={"Selected custom conditions: %d","已勾选自定义词条：%d","已勾選自訂詞條：%d"},
    scope={"Applies to: ","适用范围：","適用範圍："},
    players={"all players","全部玩家","全部玩家"}, minions={"all enemies, including elites, specialists and monsters","全部敌人，包括精英、特感和怪物","全部敵人，包括精英、特感和怪物"},
    elite={"elite enemies","精英敌人","精英敵人"}, monster={"monsters","怪物","怪物"}, special={"specialist enemies","特感敌人","特感敵人"},
    fixed_breeds={"the enemy types specified by this condition","本词条指定的敌人种类","本詞條指定的敵人種類"},
    no_description={"The author has not provided a description.","作者尚未提供文字说明。","作者尚未提供文字說明。"},
    persistent={"Persistent effects while requirements are met:","满足词条条件时持续生效：","滿足詞條條件時持續生效："},
    rule={"Trigger %d: ","触发规则 %d：","觸發規則 %d："},
    cooldown={"Cooldown %.3g s", "冷却 %.3g 秒", "冷卻 %.3g 秒"},
    delay={"Takes effect after %.3g s", "延迟 %.3g 秒生效", "延遲 %.3g 秒生效"},
    chance={"%.3g%% chance", "触发概率 %.3g%%", "觸發機率 %.3g%%"},
    limit={"Up to %d times per mission", "每局最多触发 %d 次", "每局最多觸發 %d 次"},
    global={"The trigger count and cooldown are shared by the mission.","触发次数和冷却由全局共用。","觸發次數和冷卻由全域共用。"},
    individual={"The trigger count and cooldown are tracked for each affected unit.","触发次数和冷却按受影响单位分别计算。","觸發次數和冷卻按受影響單位分別計算。"},
    interval={"Check every %.3g s", "每 %.3g 秒检查一次", "每 %.3g 秒檢查一次"},
    more={"Description %d / %d", "说明 %d / %d", "說明 %d / %d"},
    inspect={"View description", "查看说明", "查看說明"},
    empty={"No custom conditions loaded. Extract templates or refresh the DIY folder.","尚未加载自定义词条。可解压模板，或将词条包放入 DIY 目录后刷新。","尚未載入自訂詞條。可解壓模板，或將詞條套件放入 DIY 目錄後重新整理。"},
    next={"Next page", "下一页", "下一頁"}, previous={"Previous", "上一页", "上一頁"},
    unknown_stat={"Additional author-defined effect", "作者配置的其他效果", "作者設定的其他效果"},
    next_mission={"Hover to read details. Selections apply next mission; custom conditions stack when selected together.","悬停查看详细说明。勾选用于下一局；同时勾选的自定义词条会叠加生效。","懸停查看詳細說明。勾選用於下一局；同時勾選的自訂詞條會疊加生效。"},
}
local stats={
    movement_speed={"Movement speed","移动速度","移動速度"}, block_cost_multiplier={"Block stamina cost","格挡体力消耗","格擋體力消耗"},
    spread_modifier={"Weapon spread","武器散布","武器散布"}, stamina_regeneration_modifier={"Stamina regeneration","体力恢复速度","體力恢復速度"},
    melee_attack_speed={"Melee attack speed","近战攻击速度","近戰攻擊速度"}, melee_power_level_modifier={"Melee power","近战能量","近戰能量"},
    ranged_attack_speed={"Ranged attack speed","远程攻击速度","遠程攻擊速度"},
    toughness_regen_rate_modifier={"Toughness regeneration rate","韧性恢复速度","韌性恢復速度"}, toughness_damage_taken_multiplier={"Toughness damage taken","受到的韧性伤害","受到的韌性傷害"},
    corruption_taken_multiplier={"Corruption taken","受到的腐化","受到的腐化"}, recoil_modifier={"Recoil","武器后坐力","武器後座力"},
    damage_taken_multiplier={"Damage taken","受到的伤害","受到的傷害"}, ability_cooldown_modifier={"Ability cooldown","战斗技能冷却","戰鬥技能冷卻"},
    overheat_amount={"Heat generated","热量产生","熱量產生"}, power_level_modifier={"Power","能量","能量"},
    ranged_damage_taken_multiplier={"Ranged damage taken","受到的远程伤害","受到的遠程傷害"}, dodge_distance_modifier={"Dodge distance","闪避距离","閃避距離"},
    dodge_speed_multiplier={"Dodge speed","闪避速度","閃避速度"}, damage_vs_chaos_newly_infected={"Damage to newly infected","对新感染者伤害","對新感染者傷害"},
    damage_vs_chaos_poxwalker={"Damage to poxwalkers","对瘟疫行尸伤害","對瘟疫行屍傷害"}, melee_damage={"Melee damage","近战伤害","近戰傷害"},
}
local multiplicative={block_cost_multiplier=true,toughness_damage_taken_multiplier=true,corruption_taken_multiplier=true,damage_taken_multiplier=true,overheat_amount=true,ranged_damage_taken_multiplier=true,dodge_speed_multiplier=true}
local events={mission_start={"first spawn","首次生成","首次生成"},enemy_died={"enemy death","敌人死亡","敵人死亡"},on_kill={"kill an enemy","击杀敌人","擊殺敵人"},on_hit={"hit an enemy","命中敌人","命中敵人"},on_damage_dealt={"deal damage","造成伤害","造成傷害"},on_sweep_start={"start a melee swing","开始近战挥击","開始近戰揮擊"},on_syringe_used={"use a stimm","使用针剂","使用針劑"}}
local function index(mod)
    local lang=mod:localize("diy_language")
    return lang=="zh-cn" and 2 or lang=="zh-tw" and 3 or 1,lang
end
function D.word(key,mod,...)
    local n=index(mod);local value=assert(words[key],key)[n]
    return select("#",...)>0 and string.format(value,...) or value
end
function D.clean(value)
    local text=tostring(value or ""):gsub("{[^}]*}",""):gsub("<[^>]*>","")
    text=text:gsub("\\n","\n"):gsub("[\1-\8\11\12\14-\31\127]",""):gsub("`","")
    -- Drop private-use font glyphs from authored prose, retaining UTF-8 text.
    text=text:gsub("[\238\239][\128-\191][\128-\191]",function(c)
        local a,b=c:byte(1,2)
        if a==238 or a==239 and b<164 then return "" end
        return c
    end)
    return text:gsub("[ \t]+"," "):gsub(" *\n *","\n"):gsub("^%s+",""):gsub("%s+$","")
end
function D.name(entry,Schema,mod)
    local _,lang=index(mod);return D.clean(Schema.localize(entry.name,lang))
end
function D.describe(entry,library,Schema,mod)
    local n,lang=index(mod);local lines={}
    local target=entry.targets or {};local scope=target.kind=="minions" and "minions" or "players"
    if #(target.tags or {})==1 and words[target.tags[1]] then scope=target.tags[1]
    elseif #(target.breeds or {})>0 then scope="fixed_breeds" end
    lines[#lines+1]=D.word("scope",mod)..D.word(scope,mod)
    local description=D.clean(Schema.localize(entry.description,lang))
    -- These template wiring names have user-facing meanings.
    description=description:gsub("diy_pressure",n==1 and "reinforcement signal" or n==2 and "增援信号" or "增援訊號")
    description=description:gsub("f1",n==1 and "the first formation" or n==2 and "一号编队" or "一號編隊")
    lines[#lines+1]=description~="" and description or D.word("no_description",mod)
    local passive=entry.passive or {};local keys={}
    for key in pairs(passive.stats or {})do keys[#keys+1]=key end;table.sort(keys)
    if #keys>0 then
        lines[#lines+1]="";lines[#lines+1]=D.word("persistent",mod)
        local unknown=false
        for _,key in ipairs(keys)do
            local label=stats[key];local value=passive.stats[key]
            if label then
                local delta=(multiplicative[key] and value-1 or value)*100
                lines[#lines+1]=label[n]..string.format(" %+.3g%%",delta)
            else unknown=true end
        end
        if unknown then lines[#lines+1]=D.word("unknown_stat",mod) end
    end
    for i,rule in ipairs(entry.rules or {})do
        local timing={};local event=events[rule.event]
        if rule.event=="interval" then timing[#timing+1]=D.word("interval",mod,rule.interval or 1)
        elseif event then timing[#timing+1]=event[n] end
        if (rule.chance or 1)<1 then timing[#timing+1]=D.word("chance",mod,rule.chance*100) end
        if (rule.cooldown or 0)>0 then timing[#timing+1]=D.word("cooldown",mod,rule.cooldown) end
        if (rule.delay or 0)>0 then timing[#timing+1]=D.word("delay",mod,rule.delay) end
        if (rule.max_triggers or 0)>0 then timing[#timing+1]=D.word("limit",mod,rule.max_triggers) end
        if #timing>0 then lines[#lines+1]="";lines[#lines+1]=D.word("rule",mod,i)..table.concat(timing,n==1 and "; " or "；") end
        if (rule.cooldown or 0)>0 or (rule.max_triggers or 0)>0 then lines[#lines+1]=D.word(rule.scope=="global" and "global" or "individual",mod) end
    end
    local allowed,reason=library.eligible(entry)
    if not allowed and reason then lines[#lines+1]="";lines[#lines+1]=D.clean(mod:localize(reason)) end
    return table.concat(lines,"\n")
end
-- Character-aware wrapping gives the manager full, paged descriptions.
function D.pages(text,width,height)
    local pages,lines,line,used={},{},{},0
    local function flush()
        lines[#lines+1]=table.concat(line);line={};used=0
        if #lines>=height then pages[#pages+1]=table.concat(lines,"\n");lines={} end
    end
    for c in tostring(text):gmatch("[%z\1-\127\194-\244][\128-\191]*")do
        local w=(#c>1 or c:match("[MWmw@%%&]")) and 2 or 1
        if c=="\n" then flush() else
            if used+w>width then flush() end
            line[#line+1]=c;used=used+w
        end
    end
    if #line>0 then flush() end
    if #lines>0 then pages[#pages+1]=table.concat(lines,"\n") end
    if #pages==0 then pages[1]="" end
    return pages
end
return D
