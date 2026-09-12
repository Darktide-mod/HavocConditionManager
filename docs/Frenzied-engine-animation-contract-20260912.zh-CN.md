# 狂暴攻势：本机引擎动画接口的静态核查

核查日期：2026-09-12。只读分析本机 `binaries/Darktide.exe`，未附加游戏进程、注入代码或修改游戏文件。分析依赖仅放在项目 `build/engine-analysis-deps`。以下地址为该文件首选映像地址，不能用于其他版本，更不能作为模组硬编码地址。

- 文件大小：18,922,624 字节。
- SHA-256：`e0f581d2c63b692c7d9f328e3edeb39c0f484956905569d38ba27bbb3fcc0aae`。
- PE ImageBase：`0x140000000`。
- 复核工具：项目 `build/engine_animation_analysis.py`；反汇编记录位于同目录的 `engine-pending-consume.txt`、`engine-state-rebuild.txt`。

## 已确认的失效原因

`Unit.animation_set_time` 并不直接修改正在播放的动画。旧狂暴攻势只调用它，因而“setter 调用成功”和“动画播放时间已经推进”不是一回事。旧测试若让这个 setter 直接写 live time，就会掩盖这个问题。

Lua 注册点 `0x140549604` 将 `animation_set_time` 绑定到 `0x140539810`。该函数解析 unit 后的逐层数值，把 double 转为 float，写入动画实例中的待恢复数组。它不调用播放定位函数，也不写 `animation_get_time` 所读取的实时层时间。

相同实例中有两套不同存储：

| API | 已确认的存储与动作 |
| --- | --- |
| `animation_get_time(unit, table)` | 从动画实例 `+0x12e8` 指向的实时层数组读取；层步长 `0x50`，层内 `+8` 是 double 时间。读取逻辑在 `0x14053926b` 之后。 |
| `animation_set_time(unit, ...)` | 设置待恢复数组长度，向每项 `+0` 写 float 时间。数组长度位于实例 `+0xe8`，数据指针 `+0xf0`，项步长8字节。关键写入在 `0x140539a30` 至 `0x140539b37`。 |
| `animation_set_animation(unit, ...)` | 同一个待恢复数组的每项 `+4` 写 animation index；不提交播放变化。wrapper 为 `0x14053a560`，关键写入在 `0x14053a766` 至 `0x14053a7aa`。 |
| `animation_set_state(unit, ...)` | wrapper `0x14053aa20` 经 `0x1403fdda0` 调用 `0x1405a4a90`，同步消费上述待恢复数据并重建指定层。 |

因此，原版玩家动画恢复使用的 `set_time → set_animation → set_state` 顺序有实际引擎意义，并非三个可相互替代的 setter。

## 完整恢复的精确边界

`0x1405a4a90` 在存在待恢复项时逐层处理：

1. 若该层 state 为 `-1`，跳过该层。Lua 的 nil state 会被 wrapper 转换为 `-1`，因此可以只处理需要推进的层，其余层传 nil。
2. 若 animation index 为 `-1`，不把 pending time 传给重建函数。仅 `set_time + set_state` 不能可靠恢复指定播放点。
3. 对有效 state 和 animation index，读取待恢复时间，调用 `0x1405a0ff0`。没有“新旧 state 相同就跳过”的判断。
4. `0x1405a0ff0` 调用层清理函数 `0x1405a08f0`，重置该层 `0x50` 字节的实时结构、标记更新，再建立动画。后续通过 `0x1405a2460` 定位时间。
5. `0x1405a2460` 对正时间立即写回实时 double 时间，并调用底层播放器的时间定位逻辑。故 `set_state` 返回后即可用 `get_time` 检查正的目标时间是否实际写入，无需等下一次 World 更新。
6. 提交完成后，待恢复数组被清空。set_time 不应单独长期积压，以免后来的正常状态设置意外消费旧数据。

时间定位函数同时推进该层此前动画事件的索引，不能据此宣称所有音效、进入事件、根运动和配对动作均被等比播放。尤其每帧设置同一个 state 仍会重建该层，不能描述为“没有重建动画”或“完整保留过渡混合”。应只提交持续播放且需要推进的层，跳过切换、回绕和无效层，并保留游戏内验证说明。

## 其他 API 排查

- `animation_layer_info` 确实注册为 Lua API，wrapper `0x14053b5b0` 只返回实时层 `+8` double 时间与 `+4` float 值（用于时长）；没有返回底层播放器 handle。不能把返回的这两个数用作 `crossfade_animation_set_speed` 的 handle。
- `animation_get_state_layer_data` 只找到内部诊断字符串，未找到同名 Lua 注册点。不能仅凭二进制字符串存在就假设 Lua 可调用。
- `crossfade_animation_set_speed` 的 wrapper 为 `0x140535dc0`。本机实现检查 Unit 的 blender 存在，然后按第二参数 handle 查找播放器，存在时写速度；找不到时静默返回。本次没有发现该 wrapper 显式排斥 animation state machine，因此不再用“必然拒绝有状态机对象”解释它。然而，已核查的层查询 API 没有提供可安全传入的 handle；`animation_get_animation` 的资源选择 index 也不是该播放器 handle。不能猜 handle 或枚举写入代替正式接口。
- `set_simple_animation_speed` 进入独立 simple animation 资源查找路径，按可选资源名定位对象；没有证据证明它能调节敌人状态机所有层。

本次已经确认旧实现的 API 契约错误，并确认官方完整恢复调用会实际定位播放时间。尚未进行游戏内帧率、混合质量、动画事件或联机画面的验证；这些不能由静态反汇编或离线 mock 的通过结果替代。
