# 狂暴攻势：移动动画覆盖复查（2026-09-12）

## 结论与当前状态

当前 HCM 4.4.6-test.6 / 狂暴攻势 1.6.3 **没有实现所有敌人的移动动画提速**。用户观察到的掷弹兵和猎犬问题可由实际游戏资源解释，不是旧包未加载。上一版将 `anim_move_speed` 的存在和写入视为走跑提速覆盖条件，这个判断不成立。

本轮核查了原生源码中的 **50 个 minion 定义、27 个关联资源包、26 个不同动画状态机**。17 个定义使用的状态机，在编译表达式中没有发现对 `anim_move_speed` 的引用；另有三个猎犬定义，变量仅用于慢走，战斗奔跑不使用它。其余定义有变量引用，也不能据此认定每个移动片段均已覆盖。

此次更新的是审计记录与工程说明，**没有发布新的修复版，也没有修改游戏、AppData 外部包、Vortex 或原生源码**。不将尚未解决的动画问题标成修复完成。

## 日志确认

日志 `console-2026-09-12-07.51.13-59967c62-e840-4406-86fa-86d8bb187947.log` 在 07:54:06.830 记录狂暴攻势 1.6.3 激活，`move=2.00 movement_animation=native_variable traversal=native`。这排除了本次已知记录仍运行旧包的解释。

07:54:39 的攻击日志记录近战总倍率 3.00、射击总倍率 2.30；动画恢复有 1 个单位、3 个层通过时钟读回，另有 7 个层失败。此类日志只检查攻击层时钟，不能证明走跑画面提速，也不能把层数当作敌人数。

## 掷弹兵：两重缺口

`renegade_grenadier` 与 `cultist_grenadier` 共用 `content/characters/enemy/chaos_traitor_guard/third_person/animations/chaos_traitor_guard_grenadier`。

1. 两个原生 breed 都没有登记 `animation_variables`。`MinionAnimationExtension:has_variable` 只查 breed 创建的映射，并不检查底层资源；1.6.3 因而直接跳过移动变量写入。
2. 实际状态机有 `anim_move_speed`，索引 0，默认值 1。然而编译表达式里没有该变量引用。仅补登记、或直接通过 `Unit.animation_find_variable` 找到后写入，仍不能令其移动片段提速。

两个投弹兵的 `BtGrenadierFollowAction` 已在移动动作名单中。继续往动作名单添加同一个名字不会解决问题。

## 猎犬：慢走与奔跑使用不同控制

普通猎犬、猎群变体和装甲猎犬共用从 `content/characters/enemy/chaos_hound/third_person/base` 包内读取的状态机 `73334af5e4a6752c`。

- 变量表包含 `gallop_lean`（索引 0）和 `anim_move_speed`（索引 1），默认值均为 1；不是因默认值为 0 导致乘法无效。
- `walk_fwd` 片段的速度表达式为 `anim_move_speed * 0.5`。本包改动变量能影响这条慢走路径。
- `run_fwd` 是混合状态，组合三个奔跑动画，使用 `gallop_lean` 控制倾斜混合权重；其播放速度表达式为常量 1，没有读取移动速度变量。因此战斗奔跑的步频依然原速。
- `BtChaosHoundApproachAction`、`BtChaosHoundRoamAction`、`BtChaosHoundSkulkAction` 均已在移动名单中；遗漏发生在动画资源控制层。

本机资源中的可核验位置：慢走状态名在 `0xB08`，速度表达式在 `0x1032`（变量 1、0.5、乘法）；奔跑状态名在 `0x10294`，常量播放速度在 `0x107EF`，随后三条混合权重表达式读取变量 0。状态机 NaN 编码表达式包含变量令牌 `0x7F900001`、乘法令牌 `0x7F800002` 和结束令牌 `0x7FA00000`。

## 其他已确认缺口

除两种投弹兵和三种猎犬外，下列定义同样不能由当前移动变量方案完整处理：

| 类别 | 原生定义 | 资源检查 |
|---|---|---|
| 喷火兵 | cultist_flamer、renegade_flamer、renegade_flamer_mutator | 共用状态机，移动变量无编译表达式引用；前两种还缺少 breed 登记 |
| 捕网者 | renegade_netgunner | 移动变量无表达式引用，也未登记 |
| 狙击手 | renegade_sniper | 移动变量无表达式引用，也未登记 |
| 自爆兵 | chaos_poxwalker_bomber | 移动变量无表达式引用，也未登记 |
| 纳垢兽 | chaos_beast_of_nurgle | 变量已登记，但没有表达式引用 |
| 混沌卵 | chaos_spawn | 变量已登记，资源索引 23，但没有表达式引用 |
| 瘟疫欧格林 | chaos_plague_ogryn | 未登记；资源中变量默认值 0，且没有表达式引用 |
| 恶魔宿主及变体 | chaos_daemonhost、chaos_mutator_daemonhost | 未登记，变量没有表达式引用 |
| 队长及双子 | cultist_captain、renegade_captain、renegade_twin_captain、renegade_twin_captain_two | 共用状态机，变量没有表达式引用；双子还未登记 |

`attack_valkyrie` 没有这项变量，也不属于地面走跑动画。带有变量引用的普通步兵、枪手、欧格林、狂战士等列为“部分资源支持”；有引用不等于所有起步、转向、走跑及侧移片段均引用。完整 50 行清单见下表及同名 JSON。

## 同时发现的逻辑问题

1. `MinionMovement.apply_animation_wanted_movement_speed` 的本包回调，只要属于移动动作就把动画推导出的速度除以 2，以抵消导航的乘 2。它没有核实当前动画是否真的提速。因此，在未读取移动变量的起步片段上，也可能抵消本应保留的移速增益。此前离线替身假设移动片段都使用该变量，未覆盖此反例。
2. 现有离线替身默认每个单位都有移动变量、默认值 1，且移动片段播放速率正比于该变量。它验证的是这个模型下的行为；模型不符合掷弹兵与猎犬奔跑资源，不能作为这两类画面已修好的证据。
3. 攻击动画仍有恢复失败的层；当前只在第一次失败时记录总数，无法据此精确定位每个敌人与片段。移动覆盖缺口和攻击层失败应分别验证。

## 修复约束

不能通过统一写 `anim_move_speed=2` 完成本次缺口修复。需要修改未绑定片段的实际播放控制，或找到可保持混合状态及根运动的播放器速度接口，并逐状态核验。现有 `set_time → set_animation → set_state` 会重建层，不能重新无条件用于所有走跑帧，否则会引入已经观察到的起停突兀。

本机只读接口复核仍未找到能从公开查询取得有效播放器 handle 的路径；`crossfade_animation_set_speed` 需要真实 handle，动画资源选择 index 不能代替它。不以猜测 handle、关闭所有动画状态机或反复恢复所有层作为修复。

攀爬、翻越、跨沟和落地保留原生时序与几何是上一轮的明确修复决策，这些动作保持原速不属于本次遗漏。

## 方法、可复现证据与边界

- 原生 Lua 使用 Git HEAD `0f0cb45991e9305ef4a7b925370792d7d6035f95`，通过 `git show` 读取原始内容，避免工作区已有改动干扰。
- 动画资源直接从本机游戏 bundle 只读提取到工程 `build/`。关联方式为 breed 的 `state_machine` 或 `base_unit` 路径对应资源包；完整清单记录包名、状态机哈希、资源 SHA-256、变量索引、默认值及表达式引用数。
- 包读取布局参考 [darktide-extractor 的格式说明](https://github.com/ModifAmorphic/darktide-extractor/blob/bff77fe71a52fa9a2347cda50b15235cd495ad29/docs/bundle-format.md)。本轮只提取目标状态机，未改写 bundle 数据库或原始游戏资源。
- 表达式编码对照 [filediver 的状态机读取实现](https://github.com/xypwn/filediver/blob/7652e86f4765babe66874cb0b94e5784616c5c1d/stingray/state_machine/state_machine.go)，并核对本机猎犬的实际字节；没有将 Helldivers 的完整内存布局直接套用于 Darktide。
- 原生引擎允许每个动画状态使用常量或表达式作为播放速度；变量也可仅用于混合权重。[Clip State 官方说明](https://help.autodesk.com/cloudhelp/ENU/Stingray-Help/stingray_help/animation/animation_controllers/clip_state_properties.html)，[混合状态官方说明](https://help.autodesk.com/cloudhelp/ENU/Stingray-Help/stingray_help/animation/animation_controllers/custom_blend_states.html)。
- 引用计数是当前本机编译资源中相应变量令牌的计数，不是已提速片段数，更不是实机测试结果。本次没有实机逐敌人画面或远端客户端验证。

## 全部 minion 定义清单

| 原生定义 | breed 登记 | 资源默认值 | 变量表达式引用数 | 判定 |
|---|---|---:|---:|---|
| `chaos_armored_hound` | 是 | 1 | 1 | 慢走可控，奔跑固定速度 |
| `chaos_armored_infected` | 是 | 1 | 2 | 部分资源支持，不能视为全覆盖 |
| `chaos_beast_of_nurgle` | 是 | 1 | 0 | 变量未绑定表达式 |
| `chaos_daemonhost` | 否 | 1 | 0 | 变量未绑定表达式 |
| `chaos_hound` | 是 | 1 | 1 | 慢走可控，奔跑固定速度 |
| `chaos_hound_mutator` | 是 | 1 | 1 | 慢走可控，奔跑固定速度 |
| `chaos_lesser_mutated_poxwalker` | 是 | 1 | 5 | 部分资源支持，不能视为全覆盖 |
| `chaos_mutated_poxwalker` | 是 | 1 | 5 | 部分资源支持，不能视为全覆盖 |
| `chaos_mutator_daemonhost` | 否 | 1 | 0 | 变量未绑定表达式 |
| `chaos_mutator_ritualist` | 是 | 1 | 3 | 部分资源支持，不能视为全覆盖 |
| `chaos_newly_infected` | 是 | 1 | 2 | 部分资源支持，不能视为全覆盖 |
| `chaos_ogryn_bulwark` | 是 | 1 | 2 | 部分资源支持，不能视为全覆盖 |
| `chaos_ogryn_executor` | 是 | 1 | 2 | 部分资源支持，不能视为全覆盖 |
| `chaos_ogryn_gunner` | 是 | 1 | 1 | 部分资源支持，不能视为全覆盖 |
| `chaos_ogryn_houndmaster` | 是 | 1 | 2 | 部分资源支持，不能视为全覆盖 |
| `chaos_plague_ogryn` | 否 | 0 | 0 | 变量未绑定表达式 |
| `chaos_poxwalker_bomber` | 否 | 1 | 0 | 变量未绑定表达式 |
| `chaos_poxwalker` | 是 | 1 | 5 | 部分资源支持，不能视为全覆盖 |
| `chaos_spawn` | 是 | 1 | 0 | 变量未绑定表达式 |
| `cultist_assault` | 是 | 1 | 20 | 部分资源支持，不能视为全覆盖 |
| `cultist_berzerker` | 是 | 1 | 4 | 部分资源支持，不能视为全覆盖 |
| `cultist_captain` | 是 | 1 | 0 | 变量未绑定表达式 |
| `cultist_flamer` | 否 | 1 | 0 | 变量未绑定表达式 |
| `cultist_grenadier` | 否 | 1 | 0 | 变量未绑定表达式 |
| `cultist_gunner` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `cultist_melee` | 是 | 1 | 3 | 部分资源支持，不能视为全覆盖 |
| `cultist_mutant` | 是 | 1 | 6 | 部分资源支持，不能视为全覆盖 |
| `cultist_mutant_mutator` | 是 | 1 | 6 | 部分资源支持，不能视为全覆盖 |
| `cultist_ritualist` | 是 | 1 | 3 | 部分资源支持，不能视为全覆盖 |
| `cultist_shocktrooper` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `cultist_vanguard` | 是 | 1 | 12 | 部分资源支持，不能视为全覆盖 |
| `renegade_assault` | 是 | 1 | 20 | 部分资源支持，不能视为全覆盖 |
| `renegade_berzerker` | 是 | 1 | 4 | 部分资源支持，不能视为全覆盖 |
| `renegade_captain` | 是 | 1 | 0 | 变量未绑定表达式 |
| `renegade_executor` | 是 | 1 | 6 | 部分资源支持，不能视为全覆盖 |
| `renegade_flamer` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_flamer_mutator` | 是 | 1 | 0 | 变量未绑定表达式 |
| `renegade_grenadier` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_gunner` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `renegade_melee` | 是 | 1 | 20 | 部分资源支持，不能视为全覆盖 |
| `renegade_netgunner` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_plasma_gunner` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `renegade_radio_operator` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `renegade_rifleman` | 是 | 1 | 20 | 部分资源支持，不能视为全覆盖 |
| `renegade_shocktrooper` | 是 | 1 | 7 | 部分资源支持，不能视为全覆盖 |
| `renegade_sniper` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_twin_captain` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_twin_captain_two` | 否 | 1 | 0 | 变量未绑定表达式 |
| `renegade_vanguard` | 是 | 1 | 12 | 部分资源支持，不能视为全覆盖 |
| `attack_valkyrie` | 否 | — | — | 无此变量；非地面走跑 |
