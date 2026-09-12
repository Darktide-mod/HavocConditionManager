# Nexus 4.4.9 隔离检查

## 结论

用户截图与 https://www.nexusmods.com/warhammer40kdarktide/mods/1267?tab=files 显示的是通用自动安全隔离提示。提示列举可执行文件、内部扫描或 VirusTotal 命中、嵌套压缩三种可能，没有给出具体原因、命中引擎或内层文件路径。不能把其中的“嵌套压缩”选项当作实际诊断。

检查对象为 release/4.4.9/HavocConditionManager-4.4.9.zip，大小 6,711,372 字节，SHA-256 为：

`4957498ea6edc2e13828356c308cc6235f94301a39f1395b277fadaaa2f9d89b`

## 已完成检查

- ZIP 完整性及全部 CRC 通过，共 397 个文件，单一 HavocConditionManager 顶层目录。
- 实际解包后，对每个文件分别运行 7-Zip 26.00、Windows tar/libarchive 和 file/libmagic。没有成员被识别为内层压缩包；54 个游戏动画资源也没有被这两个解包器当作可打开的压缩包。
- 后缀、文件头及 ZIP 中央目录检查没有发现 ZIP、7z、RAR、gzip、bzip2、xz、CAB 等嵌套格式。Lua 内置模板采用明文字符串，未藏有压缩包。
- Microsoft Defender 对原 ZIP 执行禁止自动处理的自定义扫描，结果为“found no threats”，退出码 0。首次使用正斜杠路径的调用报错，改用 Windows 规范绝对路径后扫描成功；不把报错当作阴性结果。
- 当前发布文件仍与产品源码及 manifest 一致；未改动游戏安装、原发布 ZIP 或 Nexus 文件。

这些结果只说明本地工具没有发现嵌套压缩或 Defender 威胁，不等同于 VirusTotal 多引擎结论，也不能证明 Nexus 的内部规则不会触发。

## 需要审核的安装行为

包内没有预编译 EXE/DLL；包含两个 CMD 启动文件和一个 PowerShell 安装器。

- CMD 以当前进程的 ExecutionPolicy Bypass 调用 PowerShell，没有修改机器的长期执行策略。
- Install.ps1 使用 Add-Type 编译内嵌 C#，解析并更新游戏资源登记；完整 C# 源码就在该脚本内，不分发预编译程序集。
- 安装器只处理指定游戏目录下的 54 个动画资源补丁、资源数据库和 AppData 中的六个狂暴攻势包文件，保留备份及安装记录。游戏 EXE 仅用于 SHA-256 核验。
- 安装器核对游戏版本、原资源与载荷哈希，拒绝运行中的游戏、链接目录、路径越界、未知文件冲突和被修改的安装内容；支持升级失败回退和卸载恢复。
- 安装器没有网络下载、计划任务、服务安装、开机启动或提权请求。

上述脚本类型和动态编译是值得审核的对象，但具体隔离原因目前未知，不应断言是其中任何一项。

## 已补强的发布检查

tools/archive_guard.py 同时用于源载荷检查和最终 ZIP 成员检查，覆盖常见归档后缀、文件签名、改名 ZIP/SFX ZIP、TAR 和常见压缩流。tests/archive_guard_tests.py 包含 11 类负例，并验证原 4.4.9 正式包无嵌套归档。

## 解除隔离

Nexus 官方指引要求联系 support@nexusmods.com 或站点管理员复核，并建议保留已隔离文件，以免扰乱版本历史：
https://help.nexusmods.com/article/117-why-has-my-mod-been-quarantined

英文审核说明见 publishing/nexus-review-4.4.9.en.md。当前 GitHub 仓库按用户要求为私有，站外审核人员不能直接读取；可在发送审核申请时附上说明中列出的原始源码文件。没有发送邮件，也没有调整仓库可见性或声称 Nexus 已通过审核。
