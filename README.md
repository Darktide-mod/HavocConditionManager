[English guide](src/HavocConditionManager/docs/README.en.md) · [简体中文](src/HavocConditionManager/docs/README.zh-CN.md) · [繁體中文](src/HavocConditionManager/docs/README.zh-TW.md)

**Formal release: 4.6.1.** Apply custom Havoc ranks41–60 and EFL III/IV on authoritative Realms local hosts, and safely skip unsupported extensions in training grounds/Psykhanium. Retain the environment/EFL dropdown repair. See [EFL I–IV values and behavior](docs/efl-tiers-20261007.md) and [Nexus upload workflow](docs/nexus-automation.zh-CN.md). Live gameplay and remote-client custom-rank synchronization remain unverified.

[Nexus Main Files](https://www.nexusmods.com/warhammer40kdarktide/mods/1267?tab=files&file_id=8853) · [GitHub Release](https://github.com/Darktide-mod/HavocConditionManager/releases/tag/v4.6.1) · [Runtime installation ZIP](release/4.6.1-r2/HavocConditionManager-4.6.1.zip). English/Chinese explanations include all four EFL pacing values. File8853 is the verified primary download; all12 previous files are archived. See [Nexus publication verification](docs/validation/nexus-4.6.1-20261007.json) and [GitHub asset digest verification](docs/validation/github-4.6.1-20261007.json).

当前功能版本：4.6.1。内置「禁止医疗」直接从模组目录加载，无需解压模板；保留外部 DIY 与作者接口。「狂暴攻势」、动画资源和安装器已独立分发至 [HavocConditionPacks](https://github.com/Darktide-mod/HavocConditionPacks)。

[HCM 安装包](release/4.6.1-r2/HavocConditionManager-4.6.1.zip) · [功能与安装说明](src/HavocConditionManager/docs/README.zh-CN.md) · [帝皇之光数值说明](docs/efl-tiers-20261007.md)

死灵 UI 对应 [MortisBuffManager 4.6.2](https://github.com/Darktide-mod/MortisBuffManager/blob/main/release/4.6.2/MortisBuffManager-4.6.2.zip)。

# HavocConditionManager

4.6.1 fixes Realms local hosts silently skipping custom Havoc ranks41–60 and Emperor's Fading Light III/IV. Training grounds/Psykhanium skip unsupported extensions without an assertion and retain selections. Production SoloPlay2.6.9/Realms methods and native stat/pacing consumers are covered offline; live gameplay remains pending.

本目录是此模组唯一的活动工程。当前版本4.6.1，发布资料编号4.6.1-r2；r2仅表示说明文案修订，运行代码与本地4.6.1检查点相同。

- `src/HavocConditionManager/`：安装源码与三语说明，ZIP 中的唯一顶层目录。
- `tests/run.py`：当前原版模板架构的检查入口；历史检查文件仅用于旧版追溯，不纳入当前发布。
- `publishing/`：中英功能正文、英文简介和更新日志、版本与 Main Files 配置。
- `release/4.6.1-r2/`：独立安装 ZIP、中英 BBCode、英文简介、英文更新日志，恰好四个文件；保留历史发布目录。
- `build/checks/`：检查与验证记录；不复制到发布目录。

在本目录执行 `./Test.ps1` 检查，`./Release.ps1` 检查并打包，`./Release.ps1 -Check` 校验已有发布。已有发布目录不可覆盖。

[安装 ZIP](release/4.6.1-r2/HavocConditionManager-4.6.1.zip) · [功能与安装说明](src/HavocConditionManager/docs/README.zh-CN.md) · [发布流程](发布流程.md)

原版游戏源码与 LuaJIT 测试运行库默认位于工作区 `dev-support/`。可通过 DARKTIDE_DEV_SUPPORT、DARKTIDE_SOURCE 和 DARKTIDE_TEST_RUNTIME 指定位置。两个工程仅在联动检查中读取彼此声明的源码依赖，发布入口每次只生成本项目产物。

正式源码已移除门状态检查、Debug、生成记录和局末统计；Main Files 打包检查诊断代码残留。原版方法回归和离线界面布局检查不替代游戏内游玩测试。测试与本地打包不会部署游戏或上传 Nexus；明确执行发布工具的 `--publish` 才会上传及同步网页。

包的安装、版本、依赖、Lua 与资源接口见 [包规范](docs/diy/PACKAGES.zh-CN.md)。

外部资源接口与示例见 [资源指南](docs/diy/ASSETS.zh-CN.md)。使用外部图形时需要 SimpleAssets v2；普通词条不受影响。

## English

HavocConditionManager provides SoloPlay condition management, overall tuning, built-in No healing and external DIY loading. [HavocConditionPacks](https://github.com/Darktide-mod/HavocConditionPacks) is optional and contains Frenzied assault with its animation resources and installer. See the English guide above for installation and use. [HCM source](https://github.com/Darktide-mod/HavocConditionManager) · [Downloads](https://github.com/Darktide-mod/HavocConditionManager/releases).
