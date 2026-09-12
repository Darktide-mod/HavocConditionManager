# 狂暴攻势：原生动画调速接口核查

核查日期：2026-09-12。依据本地 Darktide 1.12.5 的 Lua 源码，固定提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`（2026-08-18）。核查读取 Git 中的原始文件，避免混入工作目录已有修改。本次仅增加核查记录，没有修改词条、安装目录或 release 包。

后续全面核查见[污染兴奋剂、毒气与各类敌人速度接口](<F:/SteamLibrary/steamapps/common/Warhammer 40,000 DARKTIDE/mod-work/havoc-redesign-20260905/projects/HavocConditionManager/docs/Enemy-speed-stim-gas-audit-20260912.zh-CN.md>)，包含 49 份品种定义、50 棵行为树和 374 个原版近战事件的离线对照。补充三点：`anim_move_speed` 的含义随动作变化；普通射击还有独立的 `minion_shoot_cooldown_modifier`；红针的 `stagger_duration_multiplier` 不能解释为自身受击硬直倍率，已查到的消费函数读取攻击方属性。本篇的“支持变量即可复用”应连同新版报告的动作分支、初始化条件和网络约束阅读。

## 结论

有可以复用的原生接口，但现有证据不能支持“一套接口让所有敌人、所有动作整体变速”的结论。

- 支持对应动画变量的敌人，走跑应使用原生 `anim_move_speed`，并与实际移动倍率配套。敌人的动画扩展已有变量同步路径。
- 玩家武器攻击原生使用 `attack_speed`，由同一个动作时间倍率驱动动画和部分判定时间。这证明玩家有完整的相关设计，但不能证明敌人动画资源也支持它。
- 在敌人品种的 `animation_variables` 声明和敌人攻击 Lua 调用中，没有找到对应的通用 `attack_speed` 用法。未声明不等于资源中绝对不存在；需要在实际加载的敌人动画控制器上进一步核查变量及其消费节点。
- 没有在本次检查的 Lua 中找到可直接套用到所有敌人动画状态机的统一播放速率 API。这里只能说明已核查的 Lua 层，不能据此断言未公开引擎内部绝无这种能力。

## 可直接复用的原生路径

| 路径 | 已确认的行为 | 使用条件 |
| --- | --- | --- |
| `MinionAnimationExtension:set_variable(name, value)` | 设置动画变量；服务器写入对应 GameObject 字段，客户端读取并应用；两端都可能按品种限制值域 | 变量必须存在于该品种的变量表，并具有对应网络字段。不能把任意新名字传给它 |
| `MinionAnimationExtension:anim_event_with_variable_float(event, name, value)` | 发送动画事件和单个变量值，已有敌人专用 RPC 和客户端处理 | 实际动画控制器必须存在并使用该变量；此事件 RPC 本身不等于持续状态和中途加入同步方案 |
| `Unit.animation_set_variable(unit, index, value)` | 设置实际动画控制器的变量 | 仅直接调用这一层不会自动完成上述联机同步，也不会创建资源中不存在的调速功能 |
| 玩家 `ActionBase.trigger_anim_event` | 读取 `weapon_action.time_scale`，向第一/第三人称动画传入 `attack_speed` 和 `action_time_offset` | 属于玩家动作与玩家动画控制器的契约，不能直接搬到敌人并假设所有挥击生效 |

原生敌人扩展：[minion_animation_extension.lua，第109、124、128、146行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/minion_animation_extension.lua#L109)。客户端事件处理：[animation_system.lua，第121行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/animation_system.lua#L121)。玩家传参：[action_base.lua，第69行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/weapon/actions/action_base.lua#L69)。

## 走跑与变种人

普通近战追击的原生实现读取移动速度属性。对缺少 `animation_variable_init.anim_move_speed` 的品种，原生代码会把大于1的移动倍率回退为1；符合条件的品种会在运行时把修改后的移动倍率写入 `anim_move_speed`。因此不能只给所有品种写同一个数，就宣称覆盖了全部走跑动画。

参考：[bt_melee_follow_target_action.lua，第31—50、202—205、212—236行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L31)。

变种人的原生冲锋确实已有步频换算：

```lua
animation_variable = wanted_charge_speed / animation_charge_speed
animation_extension:set_variable("anim_move_speed",
    math.clamp(animation_variable, min_animation_variable, max_animation_variable))
```

原生参考动画速度为8，脚本限制变量为0.9至1.2。若普通冲锋实际速度由8—12提高30%，则在保持这个参考速度的前提下，所需比值为1.3—1.95；仍保留1.2的上限就不能表达整个范围。应在词条生效期间按实际速度使用原生变量，并核查动画资源允许的范围；单纯移除脚本上限仍不等于已经验证动画资源能完整响应。

参考：[冲锋换算，第281—305行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L281)，[原生参数，第15—36行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_mutant_actions.lua#L15)。

品种并不统一。狂战士声明了 `anim_move_speed`；瘟疫欧格林的这一变量表只有 `lean` 和 `moving_attack_fwd_speed`。后者是移动攻击相关变量，不能仅凭名字把它当作整段动画的播放倍率。

参考：[狂战士，第102行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_berzerker_breed.lua#L102)，[瘟疫欧格林，第112行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_plague_ogryn_breed.lua#L112)。

## 原生敌人攻速没有完成整段挥击变速

`BtMeleeAttackAction` 读取 `melee_attack_speed`，但相关分支计算的是：

```lua
new_duration = math.max(attack_duration / melee_attack_speed,
    timing + ATTACK_SPEED_THRESHOLD_FRAME_OFFSET)
```

随后修改动作结束时刻。它保留了命中时刻之后的最低时间，没有在这段逻辑里把所有命中时间等比提前，也没有给敌人动画传入玩家那种 `attack_speed`。因此直接复用这个属性可提高攻击频率，但不足以兑现“整段攻击动画及全部判定一起加快40%”。

参考：[近战扫击分支，第259—271行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L259)，[其他近战分支，第336—348行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L336)。

远程原生 `ranged_attack_speed` 用于首次开火等待以及后续射击节奏；同样不能据此断言整段准备、装填、投掷等动画全部等比缩放。参考：[minion_attack.lua，第426—486行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/utilities/minion_attack.lua#L426)。

## 对4.4.5-test.1的修正判断

该测试版通过 `Unit.animation_get_time/animation_set_time` 在世界更新前后额外推进各层播放位置。这使用了真实存在的接口，但“设置播放位置”本身不是原生的持续调速接口。

实现为了避免把旧动画时间带入新动画，在状态/动画切换和时间回绕的帧跳过修正。因此它本身就不能保证每一帧均按目标倍率播放；同时，逐帧设置位置不能证明动画事件、根运动、音效以及配对动作都被原生引擎按相同倍率处理。它也没有新增远端客户端的播放时钟同步协议。上述是源码可确认的限制或尚未验证的事项，不能把离线计时测试通过当作游戏内完整同步已验证。

原生 `animation_set_time` 用例在玩家动画状态恢复代码中：[player_unit_animation_state.lua，第175—204行](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/utilities/player_unit_animation_state.lua#L175)。

曾核查的 `Unit.crossfade_animation_set_speed` 也不能作为现成替代。Stingray官方文档将这一组函数用于没有动画控制器、由脚本手动混合的对象；现有敌人依赖动画状态机。该文档只能解释接口类别，不能证明Darktide当前引擎暴露了相同函数：[Autodesk动画脚本接口](https://help.autodesk.com/cloudhelp/ENU/Stingray-Help/stingray_help/animation/script_interface.html)。

## 后续实现依据

1. 已支持的走跑与冲锋优先走原生变量和原生同步，按实际移动倍率计算，保留其他原生增益的基准，避免重复乘速。
2. 对不同敌人的实际动画控制器核查调速变量是否存在、哪些动作节点真正使用它。变量存在不代表所有攻击节点都使用。
3. 只有确认攻击播放倍率能生效后，才让挥击命中、动作结束、效果时点和配对动作使用相同倍率；未验证的品种不能再标为“全部同步”。
4. 在完成上述验证前，4.4.5-test.1仍应视为有已知动画覆盖问题的测试版。
