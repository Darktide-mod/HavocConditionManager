# “禁止治疗”本地词条修改

此修改是 HavocConditionManager 的独立 DIY 包，包版本 1.1.0；保留原来的 `no_healing` 条目 ID 和包命名空间。主 mod 版本不变。

按 2026-09-11 确认的规则实现：

- 开局电池已经插入的医疗站：保留医疗站与插着的电池，剩余次数置零。
- 空电池舱、附近刷新配套电池的医疗站：移除站体及其配套电池；后续加载的同类医疗站也按此规则处理。
- 医疗针剂（`syringe_corruption_pocketable`）和可拾取医疗包（`medical_crate_pocketable`）不再生成；初始化前已经生成在地图上的这两类物品会清理。
- 取消原来的 `prevent_all_healing` 关键词，角色天赋与其他治疗来源遵循原生行为。

医疗站判断使用原生“电池生成模式＋本次分配是否插入”的组合，不单看站体名称，也不根据“零次”误判为空电池舱。分配系统把电池放在附近的站会归为第二类。初始化前收到的电池生成请求会等到分配完成，避免过早判型。

电池只通过医疗站记录的关联单位处理；其他任务目标的搬运电池不受此规则影响。已插电池的站只清零初始次数，不拦截插入电池或持续锁死充能方法。

拦截作用于新地图物品，包括地图箱子、事件掉落及调用普通生成接口的 DIY 补给。已有携带物的丢弃、交换不算新增地图补给；其他三种强化针剂与弹药物品继续使用原生生成逻辑。

实现文件：[lua/main.lua](starter-conditions-no_healing/lua/main.lua)。本地包通过 HCM 已有 Lua 包接口执行，不修改公共 DIY 引擎，也不改 Vortex 管理的主 mod 文件。停用或结束任务后，拦截回到正常路径；已经移除的场景实体不会在当前任务中凭空恢复。

修改已部署到 `%APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages/starter-conditions-no_healing/`，三份文件均与通过检查的版本逐字节一致，其他词条包未修改。原包备份位于 [starter-conditions-no_healing-before-medical-map-20260911-235624](C:/Users/GDS-DESKTOP/AppData/Roaming/Fatshark/Darktide/HavocConditionManager/diy/package-backups/starter-conditions-no_healing-before-medical-map-20260911-235624)。

在大厅“DIY 词条 → 包管理”刷新，确认本项描述已更新，再勾选“禁止治疗”进入新任务。现有勾选状态保持原样。任务中刷新只影响下一局。

离线检查执行了实际安装的包校验和脚本加载器，以及参考游戏源码的医疗站初始化、插入电池、次数、物品生成与清理方法。覆盖已有/新生成的两类医疗站、分配型医疗站、早于分配的电池请求、任务电池、物品丢弃交换、房主权限、任务切换、后来加入的玩家同步和重复进入任务。图形、实体服务和网络传输使用测试替身，仍需游戏内确认视觉表现及多人同步。

检查入口：[diy_medical_map_tests.py](../tests/diy_medical_map_tests.py)。
