# 狂暴攻势 1.6.0 动画问题：本轮实机日志审计

本报告针对用户再次反馈“移速生效，但动画看起来仍是原速”的会话。它与同日较早的热更新版本冲突属于不同问题；较早报告保留在 `Frenzied-assault-log-audit-20260912.zh-CN.md`。

## 日志能够确认的结论

本轮实际运行 HCM **4.4.6-test.3** 和狂暴攻势 **1.6.0**。同一进程的两次任务均成功完成词条脚本激活，且分别打印了 `animation_clock=running updated_units=6`、`updated_units=7`。两局都是 Realms 本地监听主机。因此，本轮不能再归因于仍在运行 1.4.0，或者热更新后的版本检查中断。

然而，`animation_clock=running` 只证明旧代码调用过动画时间写入接口。该计数没有检查写入后或下一帧的时间，更没有记录实际渲染姿态、动画周期、单位种类或命中间隔。它不能推翻用户的视觉反馈，不能证明动作播放速度已经加倍，也不能单凭这个日志判断近战或远程攻击的实际频率。

## 本轮会话证据

主要日志绝对路径：

`C:\Users\GDS-DESKTOP\AppData\Roaming\Fatshark\Darktide\console_logs\console-2026-09-12-06.13.26-b4bc73c8-23e0-4b4b-bafe-15792a4534fc.log`

- 文件大小：336,481 字节。
- SHA-256：`1AD278106DACC86E255EEE7D639488AAEE0E21331423D261E0206FC464B541F1`。
- 日志第 3 行明确声明 UTC 时间；表格同时列出北京时间。

| 行号 | UTC / 北京时间 | 记录与含义 |
| --- | --- | --- |
| 4 | 06:13:26 / 14:13:26 | 新游戏进程启动。 |
| 504 | 06:13:32 / 14:13:32 | `Init DMF mod 'HavocConditionManager'`，版本 `4.4.6-test.3`。 |
| 1606、1608 | 06:14:36 / 14:14:36 | 第一局 `Booting multiplayer session as host`，Realms 创建 listen host。 |
| 1865–1874 | 06:15:00 / 14:15:00 | 注册 AiBrain、近战动画启动、扑击碰撞、移动速度、射击和 ScriptWorld 更新等钩子。 |
| 1875 | 06:15:00 / 14:15:00 | `[Frenzied assault 1.6.0] move=2.00 melee=+1.00 ranged=+1.00 special=2.00 stagger=native animation=layer_clock scope=local_authority`。这是所配置的倍率，不是实测倍率。 |
| 2300 | 06:15:01 / 14:15:01 | RealmsComputeHost：`role=host active=false render=true dedicated=false`。日志不支持将本轮归因于该模组的后台节流。 |
| 2409 | 06:15:07 / 14:15:07 | 第一局 `animation_clock=running updated_units=6`。 |
| 2450 | 06:16:06 / 14:16:06 | 第一局正常 `realms_disconnect`，`is_error: false`。 |
| 2563、2565 | 06:16:16–17 / 14:16:16–17 | 第二局再次创建本地 listen host。 |
| 2814 | 06:16:39 / 14:16:39 | 第二局再次成功激活同一 1.6.0 词条及上述倍率。 |
| 3002 | 06:16:41 / 14:16:41 | 第二局仍为本地主机，RealmsComputeHost 未激活节流。 |
| 3055 | 06:16:47 / 14:16:47 | 第二局 `animation_clock=running updated_units=7`。 |
| 3126 | 06:20:10 / 14:20:10 | 第二局正常 `quit_game`，`is_error: false`。 |

紧邻的上一份日志 `console-2026-09-12-06.12.07-8f1f7005-be6c-429f-a035-21a579e16cae.log` 第 497 行也加载 HCM 4.4.6-test.3，但没有本词条激活或动画时钟记录，不能据其评价战斗效果。

主要日志未发现 HCM `WARNING` / `ERROR`，也没有狂暴攻势 `on_activate` 失败、要求重启的版本冲突或动画 API 不可用异常。地图主题、BotJumpAssist 导航过渡、返回菜单时的视图关闭和退出时的事件回调错误没有直接指向狂暴攻势动画路径，不能作为当前故障原因。

## 实际安装文件

安装目录的 `info.json` 是 Vortex 符号链接，目录列表显示的 0 字节是链接自身长度，并非目标文件被清空。

`F:\SteamLibrary\steamapps\common\Warhammer 40,000 DARKTIDE\mods\HavocConditionManager\info.json`

链接目标：

`C:\Users\GDS-DESKTOP\AppData\Roaming\Vortex\warhammer40kdarktide\mods\HavocConditionManager-4.4.6-test.3\mods\HavocConditionManager\info.json`

该文件读取内容为 4.4.6-test.3，SHA-256 为 `DA0A268077EAAD1537E3ABB2041995E1530F1CFF049419CD3F3A174905196D5E`，与工程中不可变的 4.4.6-test.3 发布 ZIP 完全一致。实际安装的主入口 `scripts/mods/HavocConditionManager/HavocConditionManager.lua` 也与该 ZIP 相同，SHA-256 为 `C5F7D7600C5762AC169B2E9E3F7050C3A45429BDCA6F87F84B8F278529892EC2`。

实际运行的外部 DIY 实例根目录：

`C:\Users\GDS-DESKTOP\AppData\Roaming\Fatshark\Darktide\HavocConditionManager\diy\packages\starter-conditions-frenzied_assault`

该目录四个文件的修改时间都是 **14:12:41**，早于本次进程 **14:13:26** 的启动时间。`package.json` 的 `package_version` 及 `lua/main.lua:14` 的 `REVISION` 均为 **1.6.0**。

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| `package.json` | 1,666 | `16AAD6B05AF8C9C69D688CFBD4D9824D07CC6FE642C889F7AF0BB26ADE18D134` |
| `definitions.json` | 1,841 | `4C9BDB409243427DDED30B7CD37FC859A5FC942577EE7231AB945EB164DD1497` |
| `lua/main.lua` | 21,115 | `C542F8DF0DDA23A7BF853B0273DAF5940AE7C94CC27F1537517517BA321E78EB` |
| `lua/animation.lua` | 4,555 | `42E0F6CE3C7BE7D0747C14327AF1C2505DC7CC598D9AD0008B6C0366E6F89762` |

读取时，两份 Lua 文件也与本轮修改前的工程模板相同。`definitions.json` 中两项被动属性为 `melee_attack_speed=1.0`、`ranged_attack_speed=1.0`，没有仍残留 0.4 / 0.2 的情况。但配置值存在并不能代替各敌人实际调用路径的验证。

## 为什么旧诊断不充分

以下行号来自上表哈希对应的已安装 1.6.0 脚本，后续源码修复后不应套用到新版本：

1. `lua/main.lua:245–250` 在 `ScriptWorld.update` 前后调用 `AnimationSync.before/after`。
2. `lua/animation.lua:63–75` 读取更新后的分层动画时间，只在状态、动画标识一致且时间正向增加时计算补偿。
3. `lua/animation.lua:77` 调用 `Unit.animation_set_time` 后立刻将 `updated` 加一，没有读回验证。
4. `lua/main.lua:252–254` 只在整局第一次 `updated > 0` 时打印 `animation_clock=running`。

因此 `updated_units=6` 表示某一帧有 6 个单位走到了时间写入语句；它既不是整局覆盖数量，也不是成功倍速播放的单位数。没有更多日志不表示后续停止，也不表示一直有效。

另有 `animation_events` 模组钩住 `MinionAnimationExtension.anim_event_with_variable_float/anim_event`（日志 2113–2114 行）和相关 RPC（2030–2031 行）。只读检查已安装的 `mods/animation_events/scripts/mods/animation_events/animation_events_minion.lua`，其本地事件钩子执行本模组回调后按原参数调用原函数，不直接改写动画时间或 `variable_value`；RPC 分支另有事件编号缓存逻辑。这些记录不能认定它覆盖了本词条或造成冲突。

## 后续修复应验证的内容

应结合当前游戏源码核对 `ScriptWorld.update`、实际动画计算、网络同步与渲染的先后顺序，以及 `animation_set_time` 的真实用途。新的回归需要允许“接口调用返回成功，但最终姿态或后续时间推进未被改变”的情况，避免测试仅模拟理想的时间写入。

实机诊断至少需要区分设置了目标倍率、观察到动画时间推进、实际效果验证这几层含义；近战命中、开火、特殊动作释放的时点也应与动画分开衡量。现有日志中没有这些测量，不能编造实际攻击速度。

本轮审计只读取日志、安装文件和发布包，未修改游戏 mods、Vortex staging 或 AppData DIY 实例。
