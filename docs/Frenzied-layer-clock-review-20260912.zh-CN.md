# 狂暴攻势 1.6.0：动画时钟复核

核查日期：2026-09-12。原生 Lua 固定为 Darktide 1.12.5、提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`，均读取 Git 原始内容。本文是本轮只读接口审计；不把离线替身测试或日志中的 `animation_clock=running` 当作游戏内动画变速已验证。

## 已证实的调用关系

`StateGame.update` 调用 `Managers.world:update`；`WorldManager.update` 随后对活动世界调用 `ScriptWorld.update`。后者先执行 `World.update_animations` 或带回调版本，再执行 `World.update_scene` 或带回调版本。1.6.0 的 `AnimationSync.after` 在整个 `ScriptWorld.update` 返回之后才写入层时间，因此写入发生在本帧上述两阶段之后。[原生 WorldManager](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/foundation/managers/world/world_manager.lua#L137)，[原生 ScriptWorld](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/foundation/utilities/script_world.lua#L236)。

**这个时序问题不足以单独解释持续原速。** 如果 setter 真正推进了下次求值使用的播放位置，下一帧仍应累计额外进度。要判断原因，必须检查 setter 的真实消费对象，以及写入后的立即读回和后续帧是否保留。把修正移到更新之前可以改善求值时序，但不能据此保证已经修复 setter 本身的语义问题。

Autodesk 的官方说明明确指出 `update_animations_with_callback` 的回调与动画播放器更新并行执行，而不是“所有动画求值完成后的回调”。因此不能为了提前到场景更新前，就在这个回调里修改敌人的动画状态；文档也明确禁止在其中创建或销毁动画。[官方 World API](https://help.autodesk.com/cloudhelp/2019/ENU/Max-Interactive-Help/lua_ref/obj_stingray_World.html)。

## 真实的层时间用例与未验证边界

游戏 Lua 中的 `Unit.animation_get_time/set_time` 用例来自 `PlayerUnitAnimationState` 的状态恢复。原生代码按层采集时间，并在恢复时依次调用 `_override_times`、`_override_animations`、`_override_states`；时间写入使用 `Unit.animation_set_time(unit, unpack(times, 1, layer_count))`。这确认了参数形式，但不能证明“只调用 set_time”就与这组三步恢复具有相同效果，也不能证明它是完整的持续播放速率接口。[原生恢复入口](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/utilities/player_unit_animation_state.lua#L100)，[层时间恢复](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/utilities/player_unit_animation_state.lua#L175)。

1.6.0 的 `animation_clock=running` 条件是：任一单位有至少一层读到正时间增量，随后调用了 setter。它没有读回目标时间，没有检查下帧保留，也没有检查骨骼姿势。因此该日志能证明 hook 已执行，不能证明看到的动画已变快。

## 原生属性与动画同步的范围

近战的 `melee_attack_speed` 原生消费路径缩短动作结束时间，并保留命中时刻之后的最低恢复时间；它没有把整段攻击动画和全部命中时刻统一乘速。远程的 `ranged_attack_speed` 用于首次射击等待和后续射击间隔。同一个词条的移动属性生效，不能推断这些动画路径已生效。[近战恢复计算](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L259)，[远程射击计算](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/utilities/minion_attack.lua#L426)。

原生 `MinionAnimationExtension` 同步动画事件、声明的动画变量和中途加入时的状态/随机种子；本次未找到持续层时间同步。1.6.0 的播放位置修改仅发生于词条具有本地权威的实例，不能额外宣称未运行该时钟的远端客户端也同步了动画速率。[原生敌人动画扩展](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/animation/minion_animation_extension.lua#L86)。

## 不应直接替换的接口

- `crossfade_animation_set_speed` 属于无动画状态机、由脚本手工混合的动画路径；现有敌人依赖状态机，不能直接替换。[官方动画脚本接口](https://help.autodesk.com/cloudhelp/ENU/Stingray-Help/stingray_help/animation/script_interface.html)。
- `World.update_unit` 更新单位场景图，没有单单位动画时间步参数；不构成完整的动画加速方案。[官方 World API](https://help.autodesk.com/cloudhelp/2019/ENU/Max-Interactive-Help/lua_ref/obj_stingray_World.html)。
- `animation_update_units` 字符串确实存在于本地游戏可执行文件，但原生 Lua 全库没有其调用和签名。`LocomotionSystem` 仅调用全局 `MinionLocomotion.update(dt, t)`；不能从字符串名字推定一个安全的、可筛选单位的动画更新 API。[原生移动系统](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/locomotion/locomotion_system.lua#L68)。

## 本轮修复应满足的验证条件

先确认层时间 setter 如何作用于状态机与底层播放器，再选择最小实现。诊断应区分“调用写入”“写后读回一致”“下次求值保留”“同一动作段稳定达到目标进度”，日志不能混称为生效。近战、远程与特殊动作继续使用各自的单一目标倍率，避免原生属性再次缩短已经缩放的动作；实际步态、挥击及配对动作仍须游戏内观察确认。
