-- The editor and the mission compiler share this description of native fields.
-- No game template is modified by this module; paths are discovered from data.
local S = {version=3, fields={}, coarse={}, families={"pacing","roamers","hordes","specials","monsters","events","mutators","mission_events"}}
local Load=get_mod("HavocConditionManager"):io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/coordinated_load")
local Elite=get_mod("HavocConditionManager"):io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/elite_composition")

local function spec(key,en,cn,kind,min,max,step)
    S.fields[key]={key=key,en=en,cn=cn,kind=kind or "number",min=min or 0,max=max or 3600,step=step or 1}
end
local function count(key,en,cn,max) spec(key,en,cn,"number",0,max or 300,1); S.fields[key].integer=true end
local function number(key,en,cn,min,max,step) spec(key,en,cn,"number",min,max,step) end
local function chance(key,en,cn) spec(key,en,cn,"number",0,1,0.05); S.fields[key].unit="percent" end
local function flag(key,en,cn) spec(key,en,cn,"boolean") end
local function choice(key,en,cn,values) spec(key,en,cn,"choice"); S.fields[key].options=values end

number("challenge_rating_thresholds","Combat load thresholds","战斗负担阈值",0,2000,5)
number("max_tension","Maximum tension","紧张值上限",1,2000,5)
number("tension_threshold","Advance at tension","进入下一阶段的紧张值",0,2000,5)
number("tension_min_threshold","Return below tension","退回阶段的紧张值",0,2000,5)
number("decay_tension_rate","Tension decay per second","每秒紧张值衰减",0,100,0.1)
number("decay_tension_delay","Tension decay delay","紧张值衰减延迟",0,120,0.5)
number("duration","Stage duration","阶段持续时间",0,3600,1)
number("tension_modifier","Tension gain modifier","紧张值累积系数",0,20,0.1)
number("ramp_duration","Time to full escalation","达到最大加压所需时间",1,7200,10)
number("max_duration","Maximum escalation duration","最大加压持续时间",0,3600,5)
number("travel_change_pause_time","Movement pause allowance","移动变化暂停宽限",0,120,1)
number("ramp_modifiers","Maximum escalation rate","最大加压速率",0.1,10,0.1)
flag("wait_for_ramp_clear","Wait for enemies to clear","等待清场后重置")
flag("allowed_spawn_types","Allowed spawn sources","允许的刷怪来源")
flag("ramp_up_states","Stages that accumulate escalation","参与加压的阶段")
flag("wait_for_ramp_clear_reset","Stages that reset escalation","重置加压的阶段")

count("num_roamers_range","Planned enemies per zone","区域计划敌人数",1000)
number("zone_length","Zone length","区域长度",1,200,1)
count("zone_range","Zones in this density segment","当前密度区域数",200)
count("empty_zone_range","Empty zones between segments","敌群间空白区域数",200)
count("start_zone_index","First populated zone","开始布置敌人的区域",100)
number("spawn_distance","Activation distance","敌群激活距离",10,200,5)
count("num_slots","Candidate formation positions","候选队形位置数",300)
number("position_offset","Formation spacing","队形间距",0.25,20,0.25)
flag("try_fill_one_sub_zone","Prefer one subzone","优先填满一个子区域")
flag("shared_aggro_trigger","Share group alert","共享敌群警觉")
flag("use_weighted_sub_zone_positions","Weight subzone positions","按权重选择子区域位置")
count("num_encampments","Encampment allowance","驻军营地数量",32)
chance("chance_of_encampment","Encampment chance","驻军营地出现概率")
count("num_encampment_blocked_zones","Spacing between encampments","营地间隔区域数",200)
count("tag_limits","Tag allowance","兵种标签额度",300)
count("breed_limit","Breed per-group allowance","每组兵种额度",300)
count("tag_limit_bonus","Extra tag allowance","额外兵种标签额度",300)
count("max","Maximum per group","每组上限",300)
count("num_limitations_to_add_extra","Replacements before extra unit","增加特殊替换所需的超额次数",100)
chance("chance_to_skip_limits","Chance to bypass composition limits","跳过编成限制的概率")
number("faction_zone_length","Faction segment length","阵营区域长度",1,10000,10)
number("weight","Relative selection weight","相对抽取权重",0,10000,1)

number("horde_timer_range","Horde trigger interval","尸潮触发间隔",1,3600,5)
number("first_spawn_timer_modifer","First encounter interval modifier","首次遭遇间隔系数",0.05,10,0.05)
number("travel_distance_required_for_horde","Travel needed for another horde","再次尸潮所需推进距离",1,2000,5)
flag("travel_distance_spawning","Use distance based scheduling","按推进距离调度")
count("num_waves","Waves per encounter","每次遭遇波数",40)
number("time_between_waves","Time between waves","波间间隔",0.5,600,0.5)
count("max_active_hordes","Concurrent horde allowance","同时活跃尸潮上限",30)
count("max_active_minions","Active enemy threshold","场上敌人数门槛",500)
count("max_active_minions_for_ambush","Enemy threshold for ambushes","伏击潮敌人数门槛",500)
count("aggro_nearby_roamers_zone_range","Nearby zones alerted by a horde","尸潮警觉附近区域范围",20)
number("pre_stinger_delays","Warning lead","预告提前量",0,60,0.5)
number("time_to_first_wave","First wave delay","首波延迟",0,300,0.5)
chance("chance","Normal chance","普通触发概率")
chance("high_chance","Chance when extra conditions pass","额外条件满足时的概率")
count("total_num_allowed","Mission encounter allowance","整局遭遇额度",100)
flag("random_targets","Distribute targets randomly","随机分配目标")
flag("two_waves_ahead_and_behind","Split waves ahead and behind","前后分配两路波次")
flag("skip_spawners","Use hidden positions instead of spawners","使用隐藏位置放置敌群")
choice("prefered_direction","Preferred direction","优先生成方向",{"ahead","behind"})
choice("optional_prefered_spawn_direction","Preferred spawn direction","优先生成方向",{"ahead","behind"})
flag("trigger_special_coordinated_attack_on_first_wave","Coordinate specialists with first wave","首波联动特感协同")
count("trigger_special_coordinated_attack_num_breeds","Specialists in linked attack","联动特感数量",64)
number("trigger_special_coordinated_attack_timer_offset","Specialist attack offset","特感联动时间偏移",-60,300,1)
number("trickle_horde_travel_distance_range","Trickle trigger distance","小股潮触发推进距离",1,2000,5)
number("trickle_horde_cooldown","Trickle cooldown","小股潮冷却",1,3600,1)
S.fields.trickle_horde_cooldown.integer=true
count("num_trickle_waves","Waves in a trickle encounter","小股潮遭遇波数",40)
count("num_trickle_hordes_active_for_cooldown","Active groups that trigger cooldown","触发冷却的活跃敌群数",40)
count("min_players_alive","Minimum capable players","最低有效玩家人数",4)
flag("cant_be_ramped","Ignore escalation","不受逐步加压影响")
flag("not_during_terror_events","Pause during mission events","任务事件期间暂停")
flag("ignore_disallowance","Use native allowance exception","使用原版许可例外")
flag("disallow_spawning_too_close_to_other_spawn","Separate successive wave positions","分开连续波次的出生位置")
number("optional_main_path_offset","Main path offset","主路径位置偏移",0,300,5)
count("optional_num_tries","Position search attempts","位置搜索次数",100)
number("stinger_duration","Warning duration","预告持续时间",0,60,0.5)

count("max_alive_specials","Base specialist slots","基础特感槽位数",64)
number("timer_range","Normal specialist interval","普通特感调度间隔",1,3600,5)
number("spawn_failed_wait_time","Retry after failed spawn","生成失败后的重试间隔",0.5,300,0.5)
count("max_of_same","Same breed allowance","同类特感数量上限",64)
number("min_timer_diff_range","Minimum separation between slots","特感槽位的最小间隔",0,120,0.5)
number("min_distances_from_target","Minimum distance from target","距目标的最小距离",1,200,1)
number("spawners_min_range","Nearest spawner distance","出生器最小距离",1,200,1)
number("spawners_max_range","Farthest spawner distance","出生器最大距离",1,300,1)
number("max_spawn_group_offset_range","Spawn group offset","出生器组偏移范围",0,100,1)
number("optional_mainpath_offset","Path offset by specialist","特感主路径位置偏移",0,300,5)
number("foreshadow_stinger_timers","Specialist warning lead","特感预告提前量",0,60,0.5)
number("destroy_special_distance","Distant specialist cleanup distance","远离特感的回收距离",20,500,5)
flag("move_timer_when_horde_active","Advance during hordes","尸潮期间继续计时")
flag("move_timer_when_monster_active","Advance during monster fights","怪物战期间继续计时")
flag("move_timer_when_terror_event_active","Advance during mission events","任务事件期间继续计时")
number("move_timer_when_challenge_rating_above","Combat load for continued scheduling","继续计时所需战斗负担",0,1000,5)
number("move_timer_when_challenge_rating_above_delay","Delay before continued scheduling","继续计时前的延迟",0,300,1)
chance("chance_for_coordinated_strike","Specialist coordination chance","特感协同概率")
number("coordinated_strike_challenge_rating","Combat load for coordination","特感协同战斗负担要求",0,1000,1)
count("coordinated_strike_num_breeds","Specialists in coordinated attack","协同进攻特感数",64)
number("coordinated_strike_timer_range","Coordinated attack interval","协同进攻间隔",1,3600,1)
chance("coordinated_surge_chance","Surge chance","特感爆发概率")
number("coordinated_surge_timer_range","Specialist interval during surge","爆发期间特感间隔",0.5,600,0.5)
number("coordinated_surge_duration_range","Surge duration","特感爆发持续时间",1,600,1)
count("num_coordinated_surges_range","Surges per mission","整局特感爆发次数",100)
count("num_allowed_disablers_per_alive_targets","Disabler allowance by players","按有效人数设置控制型额度",64)
number("disabler_override_duration","Disabler protection duration","控制型特感保护持续时间",0,300,1)
chance("disabler_target_alone_player_chance","Chance to target an isolated player","针对独行玩家的概率")
number("rushing_distance","Separation that triggers interception","触发掉队或超前拦截的距离",1,500,5)
number("loner_time","Time alone before interception","独行多久后拦截",1,600,1)
number("speed_running_check_frequency","Speed check interval","速通检测间隔",1,120,1)
number("speed_running_required_distance","Progress per speed check","每次检测的速通推进距离",1,500,1)
count("num_required_speed_running_checks","Required consecutive speed checks","连续速通检测次数",30)
number("speed_running_required_challenge_rating","Combat load for speed interception","速通拦截所需战斗负担",0,1000,5)
for _,prefix in ipairs({"rush_prevention","loner_prevention","speed_running_prevention"}) do
    number(prefix.."_cooldown","Interception success cooldown","拦截成功后的冷却",1,3600,1)
    number(prefix.."_failed_cooldown","Interception failure cooldown","拦截失败后的冷却",1,3600,1)
end

count("num_spawns","Mission encounter count","整局遭遇数量",32)
count("num_boss_patrols_range","Elite patrol encounters","精英巡逻队遭遇数",32)
number("monster_timer_range","Timed monster interval","计时怪物遭遇间隔",1,3600,1)
count("max_allowed_by_heat","Concurrent encounters by heat stage","按热度阶段设置同时遭遇数",32)
number("pause_pacing_on_spawn","Pause other sources after spawning","生成后暂停其他来源",0,600,1)
number("pause_spawn_type_when_aggroed","Pause sources when group is alerted","敌群警觉后暂停其他来源",0,600,1)
number("despawn_distance_when_passive","Passive encounter cleanup distance","未警觉遭遇的回收距离",1,500,5)
flag("allow_witches_spawned_with_monsters","Allow daemonhosts with monsters","允许恶魔宿主与怪物并存")
flag("force_horde","Use native linked horde","使用原版联动尸潮")
chance("chance_to_spawn_monster","Specialist to monster chance","特感替换怪物概率")
chance("chance_to_spawn_monster_event","Monster replacement chance in events","事件内替换怪物概率")
count("max_monsters","Concurrent replacement monsters","同时替换怪物数",32)
number("max_monster_duration","Wait after reaching monster allowance","达到怪物额度后的等待时间",0,3600,1)
count("total_num_allowed_during_event","Replacement monsters during events","事件内替换怪物额度",100)
number("health_modifiers","Encounter health modifier","遭遇血量系数",0.05,20,0.05)

number("points_base","Base event budget","事件基础预算",0,5000,5)
number("points","Enemy group budget","敌群点数预算",0,5000,5)
number("resistance_multiplier","Event difficulty modifier","事件难度修正",0.05,10,0.05)
number("size_multipliers","Event size modifier","事件规模修正",0.05,10,0.05)
count("num_waves_by_resistance","Event waves by difficulty","按难度设置事件波数",40)
number("cooldown","Event cooldown","事件冷却",1,3600,1)
number("waves_cooldown","Event wave cooldown","事件波间冷却",0.5,600,0.5)
number("inital_cooldown_types","First event cooldown modifier","首次事件冷却修正",0.05,10,0.05)
number("weights","Composition weights","编成抽取权重",0,10000,1)
chance("chance_for_special_injection","Specialist injection chance","特感注入概率")
chance("chance_indexed_by_resistance","Injection chance by difficulty","按难度设置注入概率")
number("success_cooldown","Successful injection cooldown","注入成功后的冷却",1,3600,1)
number("failed_cooldown","Failed injection cooldown","注入失败后的冷却",1,3600,1)
flag("check_radius_to_players","Require players in event radius","要求玩家位于事件范围内")
flag("should_update_event_position","Follow event position","更新事件位置")
number("pause_pacing_on_event","Pause sources during event","事件期间暂停其他来源",0,600,1)
count("num_to_spawn","Encounter or node count","遭遇或节点数量",100)
count("num_to_spawn_per_mission","Encounter count by mission","按地图设置遭遇数量",100)
count("max_spawned_per_section","Maximum encounters per section","每区段遭遇上限",32)
number("trigger_distance","Trigger distance","触发距离",1,500,5)
number("proximity_trigger_distance","Proximity trigger radius","接近触发半径",1,200,1)
number("optional_aggro_all_within_range","Alert nearby group radius","警觉附近敌群的半径",1,300,5)

number("max_heat","Maximum heat","热度上限",1,10000,10)
number("threshold","Heat stage threshold","热度阶段阈值",0,10000,10)
number("heat_decay_rate","Heat decay per second","每秒热度衰减",0,1000,0.1)
number("player_heat_decay_rate","Player heat decay","玩家热度衰减",0,1000,0.1)
number("lowest_decay_allowed","Heat decay floor","热度衰减下限",0,10000,5)
number("heat_decay_update_frequency","Heat decay update interval","热度衰减更新间隔",0.1,60,0.1)
number("heat_multiplier","Heat gain multiplier","热度累积倍率",0,20,0.1)
number("horde_rate_multiplier","Horde accumulation rate","尸潮进度累积速率",0.1,10,0.1)
number("horde_timer_multiplier","Horde interval multiplier","尸潮间隔倍率",0.1,10,0.1)
chance("chance_spawning_ahead","Chance of spawning ahead","在前方生成的概率")
number("euclidean_distance_from_targets","Straight line distance from players","与玩家的直线距离",1,200,1)
number("main_path_distance_from_targets","Path distance from players","与玩家的主路径距离",1,300,5)
count("max_breed_amount","Same breed event allowance","事件同类兵种上限",300)
for _,key in ipairs({"num_waves","num_trickle_waves","num_waves_by_resistance","max_alive_specials"}) do S.fields[key].min=1 end
for key,d in pairs(S.fields) do
    if d.kind=="number" and not d.unit then
        if key:sub(1,4)=="num_" then -- Counts stay counts even when their names mention a cooldown.
        elseif key:find("modifier",1,true) or key:find("multiplier",1,true) or key=="inital_cooldown_types" then d.unit="multiplier"
        elseif key:find("distance",1,true) or key:find("mainpath_offset",1,true) or key:find("main_path_offset",1,true) or key=="zone_length" or key=="faction_zone_length" or key=="spawners_min_range" or key=="spawners_max_range" then d.unit="meters"
        elseif (key:find("timer",1,true) or key:find("duration",1,true) or key:find("cooldown",1,true) or key:find("time_",1,true) or key:find("delay",1,true)) and key~="move_timer_when_challenge_rating_above" then d.unit="seconds" end
    end
end

local function coarse(id,group,en,cn,description_en,description_cn,min,max,step)
    S.coarse[#S.coarse+1]={id=id,group=group,en=en,cn=cn,description_en=description_en,description_cn=description_cn,min=min or 0.25,max=max or 5,step=step or 0.25,default=1}
end
coarse("elite_density","map","Elite members per group","敌群精英人数","Scales existing elite members in horde compositions and elite patrol teams. Ordinary members keep their separate count; specialists, bosses and required objective characters are unchanged.\n\nThis adds elites instead of replacing ordinary troops. Roamer packs and point-budget events retain native selection ratios and grow with map population and event budget.","调整尸潮编成和精英巡逻队中已有精英的数量。普通成员使用独立人数设置；特感、Boss 和任务必需角色不受影响。\n\n增加精英时不再替换普通成员。沿途敌群和点数事件保留原版抽选比例，随地图人数和事件预算一起增长。",0.25,10)
coarse("roamer_population","map","Map enemy count","地图敌群数量","Controls enemies placed along the route before the squad arrives. Raising it makes populated areas denser; lowering it leaves fewer enemies to encounter.\n\nIt also increases the positions available to fit those groups. The selected faction, group composition limits and usable map space still determine how many enemies can actually be placed.","调整队伍抵达前就布置在地图沿途的敌人数量。调高后，有敌人的区域会更密集；调低后，沿途遭遇的敌人更少。\n\n可用于摆放这些敌群的位置也会随之增加。最终能布置多少人，仍取决于所选阵营、敌群编成限制和地图可用空间。",0.25,10)
coarse("encampments","map","Encampment count","驻军营地数量","Encampments are groups stationed together at selected locations along the route. This controls how many camps the map may contain: raise it for more camps or lower it for fewer.\n\nCamp size and the chance of choosing a camp location have separate settings. Setting this to 0× removes the camp allowance; maps without camps do not gain them.","驻军营地是沿途集中驻守在特定位置的一组敌人。这项调整地图允许安排的营地数：调高后可出现更多处营地，调低后更少。\n\n每处营地的人数和营地出现概率由其他设置决定。设为 0× 会取消营地额度；地图本身没有营地时，这项不会添加营地。",0,10)
coarse("patrols","map","Elite patrol count","精英巡逻队次数","Controls elite patrol encounters along the route. Raising it places more teams at unused map encounter positions, including several in a section when space permits. Lowering it plans fewer teams; 0× removes this allowance.\n\nWhen authored positions run out, remaining teams wait for later hidden positions: at least 20 seconds apart, with at most two supplemental groups active. Elite members per group adds existing elites while preserving ordinary members, formation and sounds. Mission-scripted patrols have separate settings.","调整沿途精英巡逻队的遭遇次数。调高后使用尚未占用的地图遭遇点补充队伍；空间足够时，同一分区可安排多支。调低后更少，0× 取消这部分额度。\n\n预设点位不足时，剩余额度等待后续有效遮挡位置：补入至少间隔 20 秒，同时最多保留 2 支额外队伍。敌群精英人数可增加已有精英，同时保留普通成员、阵型和音效；任务脚本巡逻使用独立设置。",0,10)
coarse("horde_size","hordes","Common enemies per horde wave","尸潮单波普通人数","Controls how many ordinary enemies are requested in each horde wave, including waves used by coordinated horde tactics. Raise it for larger waves or lower it for smaller ones.\n\nThe number of waves and the time between encounters have separate controls. Group limits and valid spawn locations can prevent a wave from reaching its requested size.","调整尸潮每一波请求生成的普通敌人数，也包括协同尸潮战术中的波次。调高后每波人数更多，调低后每波更小。\n\n一次尸潮包含多少波、多久触发一次，由其他控件调整。敌群人数限制和可用出生位置可能使实际人数少于请求数量。",0.25,10)
coarse("horde_frequency","hordes","Horde frequency","尸潮调度频率","Controls the wait and forward travel needed for another ordinary horde, plus the spacing between its waves. Raising it shortens these intervals; lowering it spreads arrivals out.\n\nAt 2.25×, a base 10-second wave gap becomes about 4.4 seconds before other pacing modifiers. Queue congestion, enemy capacity and combat pauses can still delay arrivals. Coordinated horde tactics and trickle waves retain their own timing.","同时调整普通尸潮再次触发所需的等待、推进距离，以及同一次尸潮的波间间隔。调高后衔接更紧，调低后间隔更长。\n\n设为 2.25× 时，基础 10 秒的波间隔缩短到约 4.4 秒，之后仍叠加其他节奏修正。队列积压、敌人容量和战斗暂停仍可能延后到场。协同尸潮战术和小股潮保留各自计时。",0.25,10)
coarse("horde_waves","hordes","Waves per encounter","每次尸潮波数","An ordinary horde encounter can send several waves in succession. This controls the number of waves: raise it for more follow-up waves or lower it for fewer, retaining at least one.\n\nEach wave keeps its own size and timing. Coordinated tactics use separate wave plans that can be edited in HED.","一次普通尸潮可以连续派出多波敌人。这项调整其中的波数：调高后，后续来袭波次更多；调低后更少，至少保留一波。\n\n单波人数和波间等待时间由各自设置决定。协同战术使用独立的波次计划，可在 HED 中调整。",0.25,10)
coarse("coordinated_allowance","hordes","Coordinated tactic allowance","协同战术整局额度","Coordinated horde tactics are planned attacks such as waves from both directions or a horde linked with specialists. This sets how many times each tactic may be used during a mission.\n\nRaising it allows more uses; lowering it allows fewer, with none at 0×. Each tactic must still pass its selection chance and trigger conditions; its wave plan is unchanged.","协同战术指按特定计划发起的尸潮，例如前后夹击，或尸潮与特感联动。这项调整每种战术在整局中可以使用的次数。\n\n调高后可使用更多次，调低后更少；设为 0× 会取消使用额度。战术仍须满足抽选概率和触发条件，每次的波次安排保持不变。",0,10)
coarse("coordinated_load","hordes","Coordinated combat-load ceiling","协同攻势负荷上限","Scales the native 35-point upper load limit for supported coordinated horde tactics. At 2× the ceiling is 70, and at 3× it is 105. The medium-load lower bound stays at 8.\n\nPlayer count, pacing stage and other native conditions still apply. HED rules can add requirements or explicitly replace them.","调整受支持协同攻势原本为 35 的战斗负荷上限。2× 对应 70，3× 对应 105；中等负荷的下界仍为 8。\n\n有效人数、战斗阶段和其他原版条件继续生效。HED 可追加要求或明确替换条件。",1,10)
coarse("trickle_size","trickle","Common enemies per trickle wave","小股潮单波普通人数","Trickle waves are smaller groups sent during forward travel, separate from full horde encounters. This controls the ordinary enemies in each group, including supported extra trickle waves added by conditions.\n\nRaise it for larger groups or lower it for smaller ones. Trigger timing and travel requirements have separate controls; group limits and spawn space still apply.","小股潮是在队伍推进途中陆续补入的较小敌群，独立于完整尸潮遭遇。这项调整每股普通敌人的人数，也包括支持的词条额外小股潮。\n\n调高后每股人数更多，调低后更少。触发时机和推进距离由其他设置决定，实际人数仍受敌群限制和出生空间约束。",0.25,10)
coarse("trickle_frequency","trickle","Trickle-wave frequency","小股潮触发频率","Controls the cooldown and forward travel needed to start another trickle-wave encounter: the smaller groups sent between larger fights. Raising it shortens these requirements; lowering it spaces groups farther apart.\n\nOther combat-pacing checks still apply. It does not shorten the gap between waves within a trickle encounter already running.","调整下一次小股潮遭遇所需的冷却时间和推进距离。小股潮是穿插在推进途中的较小敌群；调高后更容易接连出现，调低后两次遭遇之间的间隔更大。\n\n其他战斗节奏检查仍然生效。已经开始的一次小股潮内部，各波之间的等待时间不受这项影响。",0.25,10)
coarse("special_slots","specials","Specialist capacity","特感并行容量","Scales ordinary specialist slots, same-breed limits, player-dependent disabler allowances and coordinated attack size. Raising it permits more specialists to overlap; lowering it permits fewer.\n\nDisabler allowances remain finite and depend on the number of eligible players. For example, a baseline allowance of 1 becomes 3 at 3×. Native breed selection, protection duration, difficulty modifiers and spawn-position checks still apply.","同时调整普通特感槽位、同类上限、按有效玩家人数计算的控制型额度，以及协同特感攻击规模。调高后允许更多特感同时参与，调低后减少。\n\n控制型额度仍有限，并随有效玩家人数变化；例如基础额度为 1 时，3× 对应 3。兵种抽选、保护持续时间、难度修正和出生位置检查继续生效。",0.25,10)
coarse("special_frequency","specials","Specialist frequency","特感补充频率","Shortens ordinary specialist refill timers and slot spacing, plus coordinated attack and surge refill intervals. Raising it replenishes specialists sooner; lowering it lengthens these waits.\n\nCapacity has a separate control. Surge chance and duration, rush/loner interception timers and combat-pacing pauses retain their own settings. This does not guarantee a particular number of specialists per minute.","同时缩短普通特感补充计时、槽位间隔、协同攻击及爆发期间的补充间隔。调高后补充更快，调低后等待更久。\n\n并行人数由容量控制。爆发概率与持续时间、冲刺或落单拦截计时，以及战斗暂停保留各自设置。这项不保证固定的每分钟特感数量。",0.25,10)
coarse("special_surges","specials","Specialist surge allowance","特感爆发整局额度","A specialist surge is a temporary period of faster coordinated specialist replenishment. This controls how many such periods may occur during a mission. Raise it for more surges or lower it for fewer; 0× removes the allowance.\n\nSurge chance, duration and replenishment speed retain their own settings. Templates without this mechanism do not gain it.","特感爆发是一段临时加快协同特感补充的时期。这项调整整局允许出现多少次爆发；调高后可出现更多次，调低后更少，设为 0× 会取消爆发额度。\n\n爆发的触发概率、持续时间和期间的补充速度由各自设置决定。当前配置没有这种机制时，这项不会添加。",0,10)
coarse("monster_encounters","encounters","Map monster encounters","地图怪物遭遇数","Controls monster encounters along the route. Above 1×, unused authored encounter positions supplement the native plan, allowing several encounters per section when space permits. More encounters shorten the travel between bosses.\n\nOverflow is retained for later hidden navigation positions, at least 20 seconds apart. Supplemental bosses wait while three ordinary map monsters are alive; native pacing still applies. 0× removes this allowance. Daemonhosts, captains, specialist replacements and mission-scripted bosses have separate settings.","调整沿途怪物遭遇数量。高于 1× 时，会用尚未占用的地图预设遭遇点补足计划；空间足够时，每个分区可安排多次。遭遇增多后，Boss 之间的推进距离也会缩短。\n\n无法放入的额度会保留，之后在有效遮挡位置补入，至少间隔 20 秒。已有 3 只普通地图怪物存活时暂缓额外 Boss，原版战斗暂停仍生效。0× 取消这部分额度；恶魔宿主、队长、特感替换及任务脚本 Boss 使用独立设置。",0,10)
coarse("event_budget","encounters","Combat-event budget","战斗事件预算","Some mission fights and automatically scheduled combat events choose enemies from a pool of points. Each enemy type costs a different amount; this control changes how many points the event can spend.\n\nRaise it to allow a larger enemy force or lower it to reduce the budget. Enemy choices and their costs determine the final numbers. Mission-combat budget caps scale with it; required objective characters are excluded.","部分任务战斗和系统自动安排的战斗事件，会用一笔点数挑选敌人；不同兵种各有点数消耗。这项调整事件可以花费的总预算。\n\n调高后可投入更大规模的敌人，调低后预算减少。最终人数取决于选中了哪些兵种及其点数消耗。任务战斗的预算上限也会同步调整，完成目标所必需的角色不受影响。",0.25,10)
coarse("condition_encounters","encounters","Condition encounter count","词条专属遭遇数","Some conditions add their own encounters, such as dedicated ambushes or enemies placed at special locations. This scales the encounter counts provided by supported conditions. Raise it for more encounters or lower it for fewer, with zero at 0×.\n\nThe condition must be selected and the map must have suitable locations. Enemy buffs and the chance of triggering an encounter keep their own settings.","部分词条会额外安排专属伏击或特定位置的敌人。这项调整其中支持修改的遭遇数量：调高后请求更多次遭遇，调低后更少，设为 0× 会将相应数量降为零。\n\n对应词条必须已选中，地图也须有合适位置。敌人获得的增益和遭遇触发概率仍由词条自身决定。",0,10)
coarse("combat_tolerance","pacing","Combat capacity & load","战斗容量与负担","Scales the enemy-count and combat-load thresholds that hold back ordinary pacing. This includes horde continuation, ambush selection and the overall allocated-enemy check, which counts living enemies and queued requests.\n\nAt 3×, the base 145 allocated-enemy threshold becomes 435. A difficulty-5 horde threshold of 95 becomes 285. These are admission thresholds, not a promised on-screen count or a limit that deletes existing enemies.\n\nCombat load still uses breed-specific threat ratings. Mission pauses, tension and heat stages, spawn locations and separate scripted-event limits retain their own rules.","同时调整常规调度的人数门槛和战斗负担阈值，包括尸潮续波、伏击潮选择，以及统计存活敌人和待生成请求的总容量检查。\n\n设为 3× 时，基础 145 的总容量门槛提高到 435；难度 5 的尸潮门槛由 95 提高到 285。这些是继续安排敌人的门槛，不代表保证同屏人数，也不会删除已有敌人。\n\n战斗负担仍按各兵种的威胁评分累加。任务暂停、紧张和热度阶段、出生位置及独立脚本事件限制仍按各自规则执行。",0.25,10)
coarse("recovery_duration","pacing","Recovery duration","恢复阶段时长","Recovery is a pacing stage that usually pauses new hordes and specialists after intense fighting. This controls its end timer: raising it permits a longer recovery period; lowering it brings that timer forward.\n\nRecovery can end earlier when tension falls. Tension is a separate measure built from events such as player damage and knockdowns. This control does not start recovery immediately or clear enemies already present; the active pacing settings decide which sources pause.","恢复阶段是高压战斗后，系统通常暂停新增尸潮、特感等敌人的休整阶段。这项调整该阶段的结束计时：调高后允许休整更久，调低后计时更早结束。\n\n恢复也可能因紧张值回落而提前结束；紧张值由玩家受伤、倒地等事件累积。这项不会立即触发恢复或清除现有敌人，具体暂停哪些刷怪来源仍取决于当前节奏配置。",0.25,10)
coarse("ramp_strength","pacing","Escalation strength","持续加压强度","During pacing stages that allow escalation, continued progress can gradually speed up enemy scheduling and increase some combat-event budgets. This control scales that extra pressure above the normal rate.\n\nRaise it for stronger escalation or lower it for less. At 0× the extra escalation is removed; 1× keeps the configured curve. Escalation timing, eligible enemy sources and spawn limits retain their own settings.","在允许持续加压的战斗阶段，系统会随队伍持续推进，逐步加快部分敌人的调度，并提高部分战斗事件的投入。这项调整相对于通常状态增加的那部分压力。\n\n调高后额外加压更强，调低后更弱；设为 0× 会去掉额外加压，1× 保持默认曲线。开始加压的时机、达到峰值所需时间、参与加压的敌人来源及出生限制保持各自设置。",0,10)

function S.copy(v,seen)
    if type(v)~="table" then return v end
    seen=seen or {}; if seen[v] then return seen[v] end
    local r={}; seen[v]=r
    for k,x in pairs(v) do r[k]=S.copy(x,seen) end
    return r
end
local traditional
function S.text(d,language,description)
    local value=description and (language=="en" and d.description_en or d.description_cn) or (language=="en" and d.en or d.cn)
    value=value or d.en or d.key or d.id or ""
    if language=="tw" then
        traditional=traditional or get_mod("HavocConditionManager"):io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/template_traditional")
        value=traditional[value] or value
    end
    return value
end
function S.finite(v) return type(v)=="number" and v==v and v~=math.huge and v~=-math.huge end
function S.clamp(v,lo,hi) return math.max(lo,math.min(v,hi)) end
function S.normalize(v,definition)
    if not S.finite(v) then return definition.default or 1 end
    return S.clamp(v,definition.min,definition.max)
end
function S.coarse_config(raw)
    local result={}; raw=type(raw)=="table" and raw or {}
    for _,d in ipairs(S.coarse) do result[d.id]=S.normalize(raw[d.id],d) end
    return result
end
function S.has_coarse_changes(cfg)
    for _,d in ipairs(S.coarse) do if cfg[d.id]~=1 then return true end end
    return false
end
function S.path_key(path) local r={} for i,k in ipairs(path) do r[i]=tostring(k) end return table.concat(r,"/") end
function S.get(t,path) for _,k in ipairs(path) do if type(t)~="table" then return nil end; t=t[k] end return t end
function S.set(t,path,value)
    for i=1,#path-1 do
        if type(t[path[i]])~="table" then return false end
        -- Copy only this path. Editing one use of a shared composition does not
        -- silently edit its other uses or the global native template.
        local child={}; for k,v in pairs(t[path[i]]) do child[k]=v end
        t[path[i]]=child; t=child
    end
    t[path[#path]]=S.copy(value); return true
end
local function append(path,k) local r={} for i,v in ipairs(path) do r[i]=v end; r[#r+1]=k; return r end
S.append=append
local function range(value)
    if type(value)~="table" or #value~=2 or not S.finite(value[1]) or not S.finite(value[2]) then return false end
    for k in pairs(value) do if k~=1 and k~=2 then return false end end
    return true
end
S.is_range=range
local skip={ui=true,asset_package=true,asset_packages=true,buffs=true,buff_templates=true,horde_templates=true,fx=true,vfx=true,stingers=true,
    spawn_stingers=true,foreshadow_stingers=true,stinger_sound_events=true,pre_stinger_sound_events=true,horde_group_sound_events=true,
    sound_events=true,ambience_sfx=true,aggro_sfx=true,spawn_locations=true,levels=true,level_sizes=true,loot=true}
local children={horde_pacing_template=true,specials_pacing_template=true,monster_pacing_template=true,roamer_pacing_template=true}
local pool_keys={breeds=true,breed_names=true,breed_lists=true,rush_prevention_breeds=true,loner_prevention_breeds=true,speed_running_prevention_breeds=true,
    coordinated_strike_breeds=true,always_update_breeds=true}
local function dense(value)
    local n=0
    for k in pairs(value) do
        if type(k)~="number" or k%1~=0 or k<1 or k>#value then return false end
        n=n+1
    end
    return n==#value
end
local function breed_list(value,breeds,aliases)
    if type(value)~="table" or #value==0 or not dense(value) then return false end
    for _,v in ipairs(value) do if type(v)~="string" or not (breeds[v] or aliases and aliases[v]) then return false end end
    for k in pairs(value) do if type(k)~="number" then return false end end
    return true
end
local function composition(value,breeds)
    if type(value)~="table" or #value==0 or not dense(value) then return false end
    for _,v in ipairs(value) do if type(v)~="table" or not breeds[v.name] or not range(v.amount) then return false end end
    for k in pairs(value) do if type(k)~="number" then return false end end
    return true
end
function S.describe(root,family,breeds,boundaries)
    breeds=breeds or {}; local result,lookup={},{}; local stack={}
    local aliases=family=="specials" and root.faction_bound_breeds
    local function add(path,definition,kind,value,breed_name)
        local parent=root;local tags=root.breed_tags
        for i=1,#path-1 do parent=parent[path[i]];tags=parent.breed_tags or tags end
        local item={path=path,id=S.path_key(path),definition=definition,kind=kind,value=value,family=family,aliases=aliases,breed_name=breed_name,breed_tags=tags,parent=parent}
        result[#result+1]=item; lookup[item.id]=item
    end
    local function walk(value,path,inherited,pool_context,depth,breed_name)
        if depth>24 then return end
        if #path>0 and boundaries and boundaries[value] then return end
        if family=="mission_events" and #path==1 and (type(value)~="table" or value[1]~="spawn_by_points" or value.mission_objective_id) then return end
        local key=path[#path]; local own=type(key)=="string" and S.fields[key]
        if family=="roamers" and breeds[key] and breeds[key].breed_type=="minion" and type(value)=="number" and S.path_key(path):find("limits/",1,true) then own=S.fields.breed_limit end
        if family=="events" and (key=="captains_settings" or key=="monster_settings" or key=="twins_settings") then return end
        local definition=own or inherited
        pool_context=pool_context or pool_keys[key]
        if breeds[key] then breed_name=key end
        if type(value)=="table" and breeds[value.name] then breed_name=value.name end
        if type(value)=="table" then
            if pool_context and composition(value,breeds) then
                add(path,{key="composition",en="Enemy composition",cn="敌群编成"},"composition",value); return
            elseif pool_context and breed_list(value,breeds,aliases) then
                add(path,{key="breed_pool",en="Native breed list",cn="原版兵种列表"},"pool",value); return
            elseif definition and definition.kind=="number" and range(value) then
                add(path,definition,"range",value,breed_name); return
            end
            if stack[value] then return end; stack[value]=true
            local keys={}; for k in pairs(value) do if type(k)=="string" or type(k)=="number" then keys[#keys+1]=k end end
            table.sort(keys,function(a,b) if type(a)==type(b) then return a<b end return type(a)=="number" end)
            for _,k in ipairs(keys) do
                if not skip[k] and not (family=="pacing" and children[k]) and tostring(k):sub(1,1)~="_" then
                    local propagated=definition
                    if definition and definition.kind=="choice" then propagated=nil end
                    walk(value[k],append(path,k),propagated,pool_context,depth+1,breed_name)
                end
            end
            stack[value]=nil
        elseif definition and ((type(value)=="number" and S.finite(value) and definition.kind=="number") or (type(value)=="boolean" and definition.kind=="boolean") or (type(value)=="string" and definition.kind=="choice")) then
            -- 'max' is an allowance only inside the native roamer limit data.
            if definition.key=="max" and not S.path_key(path):find("limits",1,true) then return end
            if definition.key=="duration" and family~="pacing" then return end
            if definition.key=="threshold" and not S.path_key(path):find("heat",1,true) then return end
            -- Automatic-event composition points are a mutable accumulator,
            -- whereas mission spawn_by_points nodes contain a real budget.
            if definition.key=="points" and family~="mission_events" then return end
            add(path,definition,definition.kind,value,breed_name)
        end
    end
    walk(root,{},nil,false,0)
    return result,lookup
end

function S.scaled(item,family,cfg,breeds)
    local registry=get_mod("HavocConditionManager").template_registry
    breeds=breeds or registry and registry.breeds
    local key=item.definition.key; local path=item.id; local value=item.value; local factor,mode
    local trickle=path:find("trickle",1,true)~=nil
    local coordinated=path:find("coordinated_horde_strike_settings",1,true)~=nil
    local bias=cfg.elite_density or 1
    if item.kind=="composition" then
        if family=="hordes" or family=="mutators" then factor=trickle and cfg.trickle_size or cfg.horde_size end
        return Elite.amounts(value,bias,breeds,S.copy,factor or 1)
    elseif item.kind=="pool" then
        if family=="monsters" and path:find("breed_lists/",1,true) then
            return Elite.list(value,bias,breeds)
        end
        return value
    -- Finite roamer slots and event point pools retain native selection ratios.
    -- Their population/budget grows without trading common enemies for elites.
    elseif family=="roamers" and (key=="tag_limits" or key=="tag_limit_bonus" or key=="max" or key=="breed_limit") then factor=cfg.roamer_population
    elseif key=="num_roamers_range" or family=="roamers" and key=="num_slots" then factor=cfg.roamer_population
    elseif key=="num_encampments" then factor=cfg.encampments
    elseif key=="num_boss_patrols_range" then factor=cfg.patrols
    elseif key=="horde_timer_range" or key=="travel_distance_required_for_horde" then factor=cfg.horde_frequency; mode="inverse"
    elseif key=="time_between_waves" and family=="hordes" and not trickle and not coordinated then factor=cfg.horde_frequency; mode="inverse"
    elseif key=="num_waves" and family=="hordes" and not coordinated then factor=cfg.horde_waves
    elseif key=="total_num_allowed" and coordinated then factor=cfg.coordinated_allowance
    elseif key=="trickle_horde_travel_distance_range" or key=="trickle_horde_cooldown" then factor=cfg.trickle_frequency; mode="inverse"
    elseif key=="max_alive_specials" then factor=cfg.special_slots; mode="slots"
    elseif (key=="max_of_same" or key=="num_allowed_disablers_per_alive_targets" or key=="coordinated_strike_num_breeds") and family=="specials" then factor=cfg.special_slots
    elseif family=="specials" and (key=="timer_range" or key=="min_timer_diff_range" or key=="coordinated_strike_timer_range" or key=="coordinated_surge_timer_range") then factor=cfg.special_frequency; mode="inverse"
    elseif key=="num_coordinated_surges_range" then factor=cfg.special_surges
    elseif key=="num_spawns" and item.path[#item.path]=="monsters" then factor=cfg.monster_encounters
    elseif key=="max_allowed_by_heat" then factor=item.path[#item.path]=="boss_patrols" and cfg.patrols or item.path[#item.path]=="monsters" and cfg.monster_encounters
    elseif key=="monster_timer_range" then factor=math.max(cfg.patrols,cfg.monster_encounters); mode="inverse"
    elseif key=="points_base" and family=="events" then factor=cfg.event_budget
    elseif (key=="num_to_spawn" or key=="num_to_spawn_per_mission") and family=="mutators" then factor=cfg.condition_encounters
    elseif key=="challenge_rating_thresholds" or family=="hordes" and (key=="max_active_minions" or key=="max_active_minions_for_ambush") then factor=cfg.combat_tolerance
    elseif key=="duration" and path:find("/relax/",1,true) then factor=cfg.recovery_duration
    elseif key=="ramp_modifiers" then factor=cfg.ramp_strength; mode="ramp" end
    if not factor or factor==1 or item.kind~="number" and item.kind~="range" then return value end
    local function scale(n)
        if mode=="inverse" and n<=0 then return n end
        local changed=mode=="inverse" and n/factor or mode=="ramp" and (1+(n-1)*factor) or n*factor
        local native_fraction=mode=="inverse" and (n%1~=0 or path:find("/trickle_horde_overrides/",1,true))
        if item.definition.integer and mode~="slots" and not native_fraction then changed=math.floor(changed+0.5) end
        if key=="num_waves" then changed=math.max(1,changed) end
        local minimum=mode=="slots" and 0 or item.definition.min
        -- Native heat overrides can use subsecond cooldown multipliers below
        -- the editor's time-field minimum. Increasing frequency must not make
        -- those native values larger by clamping them up to one second.
        if mode=="inverse" and n>0 and (n<minimum or native_fraction) then minimum=0.001 end
        return S.clamp(changed,minimum,math.max(item.definition.max,n))
    end
    if type(value)=="table" then return {scale(value[1]),scale(value[2])} end
    return scale(value)
end
function S.equal(a,b)
    if type(a)~=type(b) then return false end
    if type(a)~="table" then return a==b end
    for k,v in pairs(a) do if not S.equal(v,b[k]) then return false end end
    for k in pairs(b) do if a[k]==nil then return false end end
    return true
end
function S.breed_allowed(item,id,breeds)
    local function resolve(name)
        if breeds[name] then return breeds[name] end
        local factions=item.aliases and item.aliases[name]
        if factions then for _,actual in pairs(factions) do if breeds[actual] then return breeds[actual] end end end
    end
    local breed=resolve(id)
    if not breed or breed.breed_type and breed.breed_type~="minion" then return false end
    local tags=breed.tags or {}
    local function group(name)
        local resolved=resolve(name); local t=resolved and resolved.tags or {}
        return t.monster and "monster" or t.captain and "captain" or t.special and "special" or "regular"
    end
    local wanted=group(id)
    if item.family=="specials" and item.path[1]=="breeds" then
        local subgroup=item.path[2]
        if subgroup=="disablers" and not tags.disabler then return false end
        if subgroup=="scramblers" and tags.disabler then return false end
    end
    local original={}
    for _,v in ipairs(item.value or {}) do original[group(type(v)=="table" and v.name or v)]=true end
    -- Native source types require their original breed role (ordinary troops,
    -- specialists, monsters or captains); mixing supported roles is retained.
    return original[wanted]==true
end
function S.validate_value(item,value,breeds)
    local d=item.definition
    local function valid(n) return S.finite(n) and n>=d.min and n<=d.max and (not d.integer or n%1==0) end
    if item.kind=="number" then return valid(value)
    elseif item.kind=="boolean" then return type(value)=="boolean"
    elseif item.kind=="choice" then for _,v in ipairs(d.options) do if value==v then return true end end; return false
    elseif item.kind=="range" then return range(value) and valid(value[1]) and valid(value[2]) and value[1]<=value[2]
    elseif item.kind=="pool" then
        if not breed_list(value,breeds,item.aliases) or #value>128 then return false end
        for _,id in ipairs(value) do if not S.breed_allowed(item,id,breeds) then return false end end
        return true
    elseif item.kind=="composition" then
        if not composition(value,breeds) or #value>64 then return false end
        local total=0
        for _,entry in ipairs(value) do
            for key in pairs(entry) do if key~="name" and key~="amount" then return false end end
            if not S.breed_allowed(item,entry.name,breeds) then return false end
            for _,n in ipairs(entry.amount) do if n<0 or n>300 or n%1~=0 then return false end end
            if entry.amount[1]>entry.amount[2] then return false end
            total=total+entry.amount[2]
        end
        return total>0 and total<=1000
    end
    return false
end
function S.apply(root,family,cfg,patch,breeds,boundaries)
    local items,lookup=S.describe(root,family,breeds,boundaries); local result=root; local applied,invalid=0,{}
    -- Each edited branch is copied once per compilation. Shared branches in
    -- other source paths remain separate and unchanged, as with S.set.
    local owned={}
    local function set(path,value)
        if result==root then result={}; for k,v in pairs(root) do result[k]=v end; owned[result]=true end
        local target=result
        for i=1,#path-1 do
            local key=path[i]; local child=target[key]
            if not owned[child] then
                local copy={}; for k,v in pairs(child) do copy[k]=v end
                owned[copy]=true;target[key]=copy;child=copy
            end
            target=child
        end
        target[path[#path]]=S.copy(value)
    end
    patch=type(patch)=="table" and patch or {}
    for _,item in ipairs(items) do
        local value=S.scaled(item,family,cfg,breeds)
        if patch[item.id]~=nil then
            if S.validate_value(item,patch[item.id],breeds) then value=patch[item.id] else invalid[#invalid+1]=item.id end
        end
        if not S.equal(value,item.value) then
            set(item.path,value); applied=applied+1
        end
    end
    if family=="specials" and root.max_alive_specials and not root.min_timer_diff_range and cfg.special_frequency~=1 then
        -- _setup_specials_slot falls back to a 3–5 interval even when normal
        -- timers are much shorter. Supply the same fallback at the new rate.
        set({"min_timer_diff_range"},{3/cfg.special_frequency,5/cfg.special_frequency}); applied=applied+1
    end
    applied=applied+Load.apply(root,family,cfg,set,boundaries)
    for key in pairs(patch) do if not lookup[key] then invalid[#invalid+1]=key end end
    return result,applied,invalid
end
function S.groups(items,prefix,tab)
    prefix=prefix or {}; local groups,lookup={},{}
    for _,item in ipairs(items) do
        local include=tab=="composition" and (item.kind=="pool" or item.kind=="composition" or item.definition.key=="weight" or item.definition.key=="weights")
            or tab~="composition" and item.kind~="pool" and item.kind~="composition" and item.definition.key~="weight" and item.definition.key~="weights"
        for i,k in ipairs(prefix) do if item.path[i]~=k then include=false; break end end
        if include then
            local next_key=item.path[#prefix+1]
            if next_key then
                local id=tostring(next_key); local group=lookup[id]
                if not group then group={key=next_key,path=append(prefix,next_key),count=0}; groups[#groups+1]=group; lookup[id]=group end
                group.count=group.count+1
                if #item.path==#prefix+1 then group.item=item end
            end
        end
    end
    return groups
end
return S
