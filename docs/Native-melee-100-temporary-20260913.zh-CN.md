# 原生近战 +100% 临时部署

2026-09-13，按用户要求将原生近战实验从 +20% 调整为 +100%（2 倍速度），包版本 2.1.1。已部署到 AppData 的 `HavocConditionManager/diy/packages/starter-conditions-frenzied_assault`。实验源位于 `experiments/native-melee-100`。

复用已经安装的原生动画资源，仅替换 4 个有变化的包文件。动画播放变量乘 2，配套命中、连击、扫击和动作时长除以 2。维持本地单人/机器人房间、常规近战的实验范围。

修复重新加载模块时仍保留旧动作回调的问题：每个新模块首次启用时，通过 DMF 原位替换 enter/run/leave 回调，不增加回调层数。重新启用清空动作与缺失资源缓存；旧攻击保留对应时序直到结束，新攻击使用新倍率。核心包刷新仍保留当前任务快照，下一任务使用新内容。

验证了 374 个原生 Lua 动作配置，其中 372 个按 2 倍同步。cultist_captain 和 renegade_twin_captain_two 的 attack_swing_combo_01 尚未匹配，保持原速。另通过独立模块重载、旧攻击结束、新旧清理归属、缓存重建和 10,000 次模拟 run 无动画变量访问检查。已安装的 61 个文件和 5 个原始备份逐一校验。测试未验证实机动画、资源加载器或帧率。

部署记录：`build/checks/native-melee-controller/deployment-native-melee-100-20260913.json`。

完整回退使用原安装器 `build/native-melee-20-review/install_experiment.py`，向其 `--uninstall` 传入以下新记录的绝对路径：

`build/native-melee-20-review/backups/20260913-004207-315309-native-melee-100/installation.json`

该记录包含原实验安装前的备份，可直接完整移除实验资源并恢复原词条。备份目录中的 `previous-package` 另保留升级前的 2.1.0 包。旧 +20% 安装记录、实验归档及正式发布包均保留原样；旧安装记录已被新记录取代，不能用于当前版本的直接卸载。
