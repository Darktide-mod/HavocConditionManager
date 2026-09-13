# Windows 文件接口声明冲突

修复版本：HavocConditionManager 4.4.10、HavocEnemyDirector 3.2.1、MortisBuffManager 4.6.3。

用户报告 HCM 加载 `diy_conditions.lua` 时，在文件枚举中出现：

```text
bad argument #2 to 'FindFirstFileW' (cannot convert 'struct 407 [1]' to 'struct 114 *')
```

HCM/MBM 使用 `DT_DIY_FIND_DATA`，HED 使用 `HED_TEMPLATE_FIND_DATA`。两者都具有 Windows WIN32_FIND_DATAW 的二进制布局，但原代码以同一个公开符号名声明 FindFirstFileW 和 FindNextFileW。LuaJIT 的 FFI 声明在同一个 Lua VM 中共享，后加载者不能依靠重新声明替换先前绑定的参数类型。结构体布局相同也不代表结构体指针类型兼容。

因此，HED 先枚举文件时，后启动的 HCM/MBM 可能报错；HCM 先枚举时，HED 也可能报错。测试已在真实 Windows/LuaJIT 文件接口复现后一种顺序。日志中的 407、114 是当前 VM 的内部类型编号，不是文件大小、版本或具体模组编号；仅凭编号不能确定其他玩家先加载了哪个模组。

本次修复为 Windows 文件接口添加私有 FFI 名称，以 LuaJIT 支持的 `__asm__("Windows符号名")` 声明直接解析原 kernel32 导出。DIY 读取器使用 `DT_DIY_IO_`，HED 使用 `HED_TEMPLATE_IO_`。它们不再争用公开的函数声明，也不会覆盖其他模组的接口类型。结构体存在检查与函数别名声明分开处理，兼容旧版结构体已留在 VM 中的重新加载。

这里的 `__asm__` 是符号名称映射，不是执行汇编代码、扫描内存或修改机器码。仍然直接调用原有 Windows API，不增加每帧任务、文件访问次数或外部进程。

测试 `tests/filesystem_ffi_tests.py` 覆盖三者的全部六种加载顺序，每种顺序分别在干净 VM、其他模组先声明接口、旧版结构体与外部接口都存在的 VM 中运行，共 18 种组合；每个 VM 重新加载两遍。验证实际中文目录/文件名、首次及后续文件枚举、读写与覆盖、包目录遍历、备份、导出，以及外部接口声明保持可用。三项目的完整回归检查通过。

更新已有的三个模组后重新启动游戏，让此前初始化失败的模组重新完整加载。无需调整加载顺序、删除 AppData 配置或清理用户词条。已正确安装 4.4.9 动画资源的用户无需重新安装资源；本次没有修改动画载荷或狂暴攻势参数。

实际其他玩家环境的复测仍待反馈。技术参考：[LuaJIT FFI Semantics](https://luajit.org/ext_ffi_semantics.html)。
