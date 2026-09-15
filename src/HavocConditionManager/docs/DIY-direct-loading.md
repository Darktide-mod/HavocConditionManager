# 内置和外部 DIY 词条

内置包位于 `mods/HavocConditionManager/diy/packages`，由同目录上一级的 `index.json` 声明，直接读取 JSON / Lua，不解压、不复制。当前内置「禁止医疗」。管理器中不能卸载内置包，效果仍需在词条配置中勾选。

外部目录保持 `%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages`。每个文件夹放一个标准 DIY 包；在大厅刷新后，下一局使用新内容。刷新清理派生缓存，进行中的任务继续使用自己的快照。包内 Lua 不在扫描时执行。

优先顺序为 HCM 内置包、已注册集合包、AppData 外部目录。同 ID 的旧副本不重复加载，原文件保留并在管理器提示。不同 ID 使用冲突命名空间时仍按包验证规则报告冲突。

扩展集合使用 `diy_api.register_package_source(mod_name)` 注册自己的 `mods/<mod_name>/diy/index.json`。索引格式为 `{"version":1,"packages":["package-id"]}`，包位于同目录的 `packages/package-id`。包清单中的 `files` 必须完整列出文件。停用集合时调用 `diy_api.unregister_package_source(mod_name)`；不改变本局已经冻结的词条。

狂暴攻势与动画安装器移到独立的 [HavocConditionPacks](https://github.com/Darktide-mod/HavocConditionPacks)。HCM 主包仅保留接口，不包含动画补丁、PowerShell/CMD 安装器、EXE 或 DLL。此调整不能预先保证 Nexus 的扫描结果。

旧版升级请关闭游戏后替换旧 HCM 模组文件夹，避免旧脚本和动画资源文件残留在该文件夹。AppData 设置、外部词条、旧动画安装记录均保留；已经注册到游戏中的动画补丁不由 HCM 升级自动卸载。扩展集合保留其校验和卸载兼容流程。

## English

Built-ins load directly from `mods/HavocConditionManager/diy/packages`; no extraction is performed. No healing remains built in. Built-in packages cannot be unloaded in the manager, but their effects still require selection. External packages retain their AppData path. Companion mods register their fixed declared directory through `register_package_source` and unregister it on disable. Same-ID older copies remain on disk and are shadowed by the declared source. Refresh applies to the next mission and never executes package Lua or replaces active mission snapshots.
