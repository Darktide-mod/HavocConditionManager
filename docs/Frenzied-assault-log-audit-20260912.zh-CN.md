# 狂暴攻势实机日志审计（2026-09-12）

## 结论

13:47 启动的游戏进程实际先运行了旧的狂暴攻势 **1.4.0**；两局之间磁盘上的 DIY 包变成了 **1.5.1**，但进程仍持有 1.4.0 安装的钩子。第二局因此在 `on_activate` 中触发版本检查并终止脚本初始化。这是日志能够直接证明的失效原因，不能简单归因于增幅不明显。

第二局失效的是脚本控制的移速、动作数据缩时、特殊动作处理和动画推进。词条定义中的被动属性 `melee_attack_speed=0.4`、`ranged_attack_speed=0.2` 不会因为这个脚本错误自动移除，仍可能通过游戏原生支持的路径生效。因此不能声称第二局整个词条的所有效果都消失了。

首局记录了 `animation_clock=running updated_units=11`，说明旧版脚本至少运行到了单位动画处理路径；它不证明肉眼呈现、所有敌人、所有攻击都正确。首局实际进入运行阶段后很快退出，不能据此充分验证旧版行为。

## 会话与证据

日志目录：`C:\Users\GDS-DESKTOP\AppData\Roaming\Fatshark\Darktide\console_logs`。文件中的时间是 UTC，下面同时列出北京时间（UTC+8）。

主要日志：`console-2026-09-12-05.47.46-c2da231a-ca09-4db3-bb36-10dada62be7f.log`，331,066 字节。

| 行号 | 日志时间 / 北京时间 | 证据与含义 |
| --- | --- | --- |
| 499 | 05:47:52 / 13:47:52 | 主模组版本为 `4.4.6-test.2`。主模组版本与已解包 DIY 实例版本是两个不同层次。 |
| 1618 | 05:48:28 / 13:48:28 | `Booting multiplayer session as host`；首局为本地主机。 |
| 1887–1896 | 05:48:56 / 13:48:56 | 安装 AiBrain、攻击、移动和世界更新等狂暴攻势钩子。 |
| 1897 | 05:48:56 / 13:48:56 | 明确打印 `[Frenzied assault 1.4.0] move=1.30 attack=+0.40 ... scope=local_authority`，并非发布包内的新 1.5.1 实现。 |
| 2445 | 05:49:04 / 13:49:04 | `[Frenzied assault 1.4.0] animation_clock=running updated_units=11`。 |
| 2446–2448 | 05:49:05 / 13:49:05 | 以 `realms_disconnect` 正常退出首局。 |
| 2583 | 05:49:26 / 13:49:26 | 第二局再次以本地主机启动。 |
| 2825 | 05:49:49 / 13:49:49 | `frenzied_assault/on_activate: DIY/starter-conditions-frenzied_assault/lua/main.lua:137: Frenzied assault was updated: restart the game before starting another mission`。 |
| 3124–3126 | 05:51:55 / 13:51:55 | 第二局以 `quit_game` 退出；中间没有成功激活 1.5.1 或动画处理恢复的记录。 |

该日志只有上述一次 HCM WARNING，没有 HCM ERROR，也没有狂暴攻势动画 API 不可用的错误。地图主题、导航过渡等其他错误没有指向这次版本检查，不能作为词条失效原因。

## 磁盘实例与加载方式

实际 DIY 实例位于：

`C:\Users\GDS-DESKTOP\AppData\Roaming\Fatshark\Darktide\HavocConditionManager\diy\packages\starter-conditions-frenzied_assault`

审计时该实例：

- `package.json` 的 `package_version` 为 `1.5.1`。
- `lua/main.lua:14` 的 `REVISION` 为 `1.5.1`。
- `lua/main.lua` 的创建和修改时间均为 **13:49:23**，处在两局之间。
- `lua/main.lua` 与 1.5.1 工程源码的 SHA-256 相同：`57A9C432091888C2D6EC89FE40EB0A00814E129B7589175FF386A7EBA70261C7`。

这与“第一局运行旧实例，第二局读取新实例”吻合。具体是点击“解压模板 DIY 词条”还是外部替换文件，日志没有记载，不能断言操作者或具体操作。

主模组安装在游戏的 `mods\HavocConditionManager`，读取到版本 `4.4.6-test.2`，文件由 Vortex 符号链接管理。内置模板由 `diy_package_library.lua:144–164` 的 `extract_templates()` 明确写入磁盘并刷新；仅升级主模组不等于已解包实例自动升级。界面说明 `diy_condition_details.lua:9` 也明确表达了解压覆盖和立即加载行为。

## 为什么第二局无法恢复

以下行号以审计时的 1.5.1 实现及 test.2 DIY 引擎为准：

1. 实例 `lua/main.lua:134–140` 读取进程内的 `mod._diy_frenzied_assault_hooks_v1`；若已有状态且版本不同，立即抛出要求重启的错误。
2. 第一局遗留的钩子状态版本是 1.4.0；第二局脚本版本是 1.5.1。检查发生在新的 `current` 控制器建立前。
3. `diy/diy_scripts.lua:132–143` 捕获该错误，将脚本绑定设为不活跃，并执行 `engine.clear_script()`。没有初始化新的移动记录、动作计时控制器或动画推进控制器。
4. `diy/diy_engine.lua:115–116` 的 `clear_script()` 只清除脚本效果。`diy_engine.lua:348–352` 仍独立叠加所选词条的 `passive`，所以该错误不会自动关闭原生被动攻速。

该检查防止在旧钩子仍存在时混用不同实现，但错误仅写入日志会使玩家难以理解“已选词条却没有完整效果”的状态。修复需要同时处理模板更新后的可运行状态和更清楚的生效诊断，不能只调高数值。

## 新会话的读取边界

另有 `console-2026-09-12-05.57.43-7859e855-da0a-40af-9e4f-c6869f778e62.log`。第一次检查时它为 0 字节，无法分析；最终读取时为 **226,216 字节**，最后写入时间为 **14:00:00**，已经出现 `[Log end]`。

- 497 行：启动主模组 `4.4.6-test.2`。
- 593 行：启动 MortisBuffManager `4.6.0`。
- 1611 行：13:58:22 开始本地主机会话。
- 1946–1952 行：14:00:00 收到退出应用信号，开始销毁 `RealmsPreparationState`，`shutdown=true`。
- 1959、2171 行：关闭时发生 `ui_view_handler.lua:131: attempt to index local 'view_data' (a nil value)`。
- 2175–2176 行：栈指向 `realms_loadout/workspace_shell.lua:154` 的 `_close_page` 和 `:223` 的 `on_exit`；2187 行显示要关闭的视图为 `mbm_workspace_mortis_catalog_view`，其 `view_data=nil`。

该新会话没有狂暴攻势激活、动画处理或版本错误记录，不能据此判定重启后的 1.5.1 成功或失败。上述异常发生在退出应用、销毁 UI 时，指向已不存在的 Mortis 子视图被关闭；它是独立于狂暴攻势的退出路径问题，不应混入速度词条失效结论。

本次审计仅读取日志、安装文件和 DIY 实例；未修改游戏安装、Vortex 或 AppData。报告不能替代后续的真实游戏行为与动画观感验证。
