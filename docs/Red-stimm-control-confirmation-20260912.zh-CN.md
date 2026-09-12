# 红针的攻速与抗控制效果复核

日期：2026-09-12。核对对象：敌人用原版 `mutator_stimmed_minion_red`，不是玩家战斗兴奋剂。源码版本：Darktide 1.12.5，提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。源码均从 Git 提交读取。

## 结论

红针同时有近战攻速属性和很强的抗踉跄效果。它没有让整段挥击动画以 1.4 倍速度播放；许多连续攻击内部的出手时点也不改变。因此“敌人更难被打断，但看不出挥刀加快”与源码一致。不能把它概括成所有攻击实际快 40%，也不能把它概括成完全免疫所有控制。

## 实际消费路径

| 配置 | 原版实现与限制 |
| --- | --- |
| `melee_attack_speed = 0.4` | 原版增益结算得到 1.4。近战行为进入时读取，通常缩短行为结束前的剩余等待；不提前原来的命中时点，也不设置动画播放倍率。被格挡后的恢复行为也读取该属性。 |
| `impact_modifier = -2` | 原版基础值为 1，加法结算后是 -1，没有在增益结算中截断为零。目标方的该属性进入踉跄冲击力计算，显著削弱普通受击产生的踉跄。攻击者的额外冲击加成、动作免疫、强制踉跄和特殊覆盖仍会影响结果。 |
| `stagger_duration_multiplier = 0.1` | 原版普通 minion 踉跄应用函数读取的是攻击者的该属性，不能解释成红针目标受到的硬直时间缩短 90%。 |
| `stimmed` 与攻击许可 | 保留红针原版关键词、特效与攻击许可逻辑。红针模板没有 `no_stagger` 或 `stun_immune`；强制踉跄入口不读取冲击力属性，不能据此宣称完全免控。 |

近战行为的结束时间使用：

`max(原行为时长 / 1.4, 末次攻击时点 + 0.2666667 秒)`

这项下限会使连击受益很小。例如 `renegade_berzerker / attack_combo_01`，首击仍在约 0.747 秒，行为结束从约 3.733 秒变成 3.573 秒，仅提前 0.160 秒。它不是连击动画整体加快 40%。这些时间是动作行为数据与原版计算结果，不是实机两次命中间隔的测量。

## 源码位置

以下均为上述提交中的路径：

- `scripts/settings/havoc/havoc_mutator_local_settings.lua:375`：红针三项属性。
- `scripts/settings/buff/havoc_buff_templates.lua:1654`：红针模板、关键词、攻击许可和特效。
- `scripts/settings/buff/buff_settings.lua` 与 `scripts/extension_systems/buff/buffs/buff.lua:689`：属性类型、基础值及无截断的原版叠加。
- `scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua:336`：近战结束时间计算。
- `scripts/utilities/attack/stagger_calculation.lua:190`：目标与攻击者冲击属性参与踉跄计算。
- `scripts/utilities/attack/stagger.lua:144`：强制踉跄检查；`_apply_stagger` 中的时长倍率来自攻击者。

## 本地核验

最近日志 `console-2026-09-12-14.50.54-4987d36b-3a41-4390-8790-2db91399045f.log` 确认加载 HCM 4.4.7；外部狂暴攻势包为 2.0.0，入口脚本与发布版哈希一致。未发现相关脚本异常，但未开启逐敌人诊断，因此日志本身不能证明实机攻速变化幅度。

本次隔离执行了原版属性叠加、踉跄冲击修正及强制踉跄方法，确认红针结算为近战 1.4、冲击 -1、时长 0.1；普通默认冲击修正从 1 变为 -1；红针关键词不会阻止强制踉跄，而 `no_stagger` 对照会阻止。引擎对象在测试边界被模拟。

结果：`build/checks/red-stimm-control-confirmation.json`。已有原版近战计时检查见 `build/checks/frenzied-red-stimm.json`；动作对照见 `docs/Native-melee-timing-comparison-20260912.zh-CN.md`。

本次只复核并补充说明，没有改变当前词条或发布包。

