# 渣滓狂战士历史攻速上调核查

核查日期：2026-09-12。目标为渣滓狂战士 Dreg Rager，脚本名 `cultist_berzerker`；血痂狂战士是 `renegade_berzerker`。

## 确认版本

上调发生在 **2024-06-25 的 1.4.0《Secrets of the Machine God》**。官方公告在 2024-06-28 的补充说明中明确写出：为了区分两种狂战士，渣滓狂战士的连击变快。这是补记发布日期，不是改动首次上线日期。[Fatshark 官方公告](https://forums.fatsharkgames.com/t/secrets-of-the-machine-god-out-now-pt-2/96132/1)

版本定位采用公告与游戏脚本历史快照交叉核对。Aussiemon 仓库是社区保存的发行版反编译脚本历史，不是 Fatshark 公开的内部 Git 仓库；可以检查游戏发行脚本的变化，不能据此声称取得官方动画制作工程。

| 快照 | 提交 | 用途 |
| --- | --- | --- |
| 1.3.11，2024-05-30 | `c26228b23b962cb4986350b25e39d6cbdb1d3c73` | 上调前最近的发行快照 |
| 1.4.0，2024-06-25 | `fffa35ad098eb56d9dd879949c7f636a76a4afef` | 上调后的发行快照 |
| 1.6.0，2024-12-03 | `cc8f8846b49365a77fca1c14efdb734be05d66ea` | 后续减速调整 |
| 1.7.1，2025-03-27 | `edcd85d1e749be60c147cb428da06ed4eb1cd7a3` | 核验后续记录；这份动作文件的此次变化仅增加 disable 配置 |
| 1.12.5，2026-08-18 | `0f0cb45991e9305ef4a7b925370792d7d6035f95` | 本地当前原版参考；继续使用 fast 事件，但部分时间后来又有变化 |

## 1.4.0 实际改了什么

### 1. 更换连击动画事件

普通连击选择由 `attack_combo_01 / 04 / 08` 改为 `attack_move_combo_01_fast / 08_fast`。04 号改成 `attack_move_combo_04_fast`，并移至新的 `leap_attack` 行为。

这里的 leap_attack 仍由已有的 `BtMeleeAttackAction` 执行，不是猎犬扑咬或爆破手的专用扑跃类。行为树增加了该节点，选择条件考虑距离、高差、视线和攻击槽位。

参考：[1.3.11 动作配置](https://github.com/Aussiemon/Darktide-Source-Code/blob/c26228b23b962cb4986350b25e39d6cbdb1d3c73/scripts/settings/breed/breed_actions/cultist/cultist_berzerker_actions.lua#L306)、[1.4.0 动作配置](https://github.com/Aussiemon/Darktide-Source-Code/blob/fffa35ad098eb56d9dd879949c7f636a76a4afef/scripts/settings/breed/breed_actions/cultist/cultist_berzerker_actions.lua#L306)、[1.4.0 行为树](https://github.com/Aussiemon/Darktide-Source-Code/blob/fffa35ad098eb56d9dd879949c7f636a76a4afef/scripts/extension_systems/behavior/trees/cultist/cultist_berzerker_behavior_tree.lua#L39)。

### 2. 同步提前全部命中时点与动作结束时间

下表按原版 Lua 数据计算，单位为秒；速度变化相对 1.3.11，同名编号的动作映射用于比较。

| 连击 | 首次命中：旧 → 新 | 行为总时长：旧 → 新 | 时序对应速度变化 |
| --- | --- | --- | --- |
| 01 | 0.746667 → 0.583333 | 3.733333 → 2.916667 | +28% |
| 04，改为突进攻击 | 0.566667 → 0.472222 | 3.266667 → 2.722222 | +20% |
| 08 | 0.600000 → 0.500000 | 3.666667 → 3.055556 | +20% |

分别执行两版原始动作配置后验证：这三组的每一个命中时间都与总时长按同一倍率缩短，误差小于 1e-10。此处不是只提前第一次命中，也不是只缩短结束等待。

同时，普通近战中部分 `attack_anim_durations` 变短，例如 attack_01 从 1.166667 到 0.933333；该普通动作的命中时点没有变化。不能将连击的整体时序变化套用到每一种普通攻击。

### 3. 配套调整攻击中位移

`animation_move_speed_configs` 同时更新。例如 01 连击的 distance 档位从 4.6/3.5/3.2/2.5/0.8，变为 2.6/2.5/2.2/1.5/0.8；这些用于攻击中距离与动画移动变量的映射，不能当成全体走跑速度倍率。04 号还具有独立的突进选择条件与位移配置。

### 4. 继续使用原有执行与同步路径

1.3.11 与 1.4.0 的以下文件逐字相同：

- `bt_melee_attack_action.lua`
- `minion_animation_extension.lua`
- `cultist_berzerker_breed.lua`

已有近战执行器从动作配置选事件，调用 `animation_extension:anim_event(attack_event)`，再读取同一事件对应的命中时点和结束时间。已有动画扩展调用引擎 `Unit.animation_event`，服务器发送原生动画事件 RPC。

所以在本次核对的 Lua 范围内，此改动是静态动作配置与已有动画事件配套，不需要新增逐帧扫描、内存读取或动画恢复循环。这不等于游戏动画计算本身零开销，也不等于已经测得实际帧率。[当时的近战执行器](https://github.com/Aussiemon/Darktide-Source-Code/blob/fffa35ad098eb56d9dd879949c7f636a76a4afef/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua)、[当时的动画扩展](https://github.com/Aussiemon/Darktide-Source-Code/blob/fffa35ad098eb56d9dd879949c7f636a76a4afef/scripts/extension_systems/animation/minion_animation_extension.lua)。

## 后续调整

2024-12-03 的 1.6.0《Grim Protocols》官方公告明确提到下调渣滓狂战士连击速度。[官方公告](https://forums.fatsharkgames.com/t/grim-protocols-patch-notes-pt-2/102289/1)

脚本中仍保留 fast 事件名，但 01 总时长改为 3.888889 秒，08 改为 3.666667 秒，相应命中时点也后移。04 突进攻击的这些时间未在该次差异中改变。可见事件名字中的 fast 不代表永久固定的倍率。

当前 1.12.5 的 01 与 08 总时长分别为 3.333333、3.055556 秒。不能直接拿当前文件当作 2024 年刚上调时的完整状态。本次没有将当前这些数值再次上调的版本定位到单一发行版。

## 对狂暴攻势实现的意义

历史改动证明存在“特定快速动画事件 + 与之匹配的完整攻击时序”这条原版路径。它和红针的 `melee_attack_speed` 消费方式不同：后者主要改变行为结束等待，不推进原有每次命中时点。

如复用已存在的快速事件，应同时使用对应判定时间和位移配置。这种静态配置路径能避免模组额外的逐帧调速维护。对于没有匹配快速状态的其他敌人，不能只给事件名加 fast 或只缩短命中表，便宣称动画同步或全体通用。

没有取得 2024 年两个版本的动画控制器/动画二进制资源，因此目前可以确认 Lua 切换到专用 fast 动画事件，不能进一步断言当时资源内部是修改固定播放倍率、重烘焙动画还是其他制作方式。本地当前控制器的已有解析器也未能完整解析该共享控制器；这不作为历史资源倍率的证据。

## 核查材料

位于 `build/checks/dreg-rager-history/`：

- `audit.py`：下载固定提交快照，执行原版动作数据，核对全部命中时点比例。
- `result.json`：数值、提交、源文件哈希及限制。
- 各版本文件与逐文件差异，均保存于分析目录。

本次没有修改产品代码、游戏安装、外部词条、现有发布包，也没有启用游戏诊断日志。
