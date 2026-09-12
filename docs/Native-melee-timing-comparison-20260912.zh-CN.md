# 原版近战：1.0 与 1.4 攻速的 374 个事件对照

固定提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。主报告：[红针为何提高攻击频率](<F:/SteamLibrary/steamapps/common/Warhammer 40,000 DARKTIDE/mod-work/havoc-redesign-20260905/projects/HavocConditionManager/docs/Enemy-speed-stim-gas-audit-20260912.zh-CN.md>)。

将实际原版动作的计时表交给未修改的近战 enter/_start_attack_anim 方法，比较最终近战攻速属性为 1 和 1.4 时的结果。没有给每一种敌人实际添加红针；因此这张表表示“红针对应倍率作用于该通用近战路径”的结果，不表示所有这些敌人原版都会打红针。

40 份动作数据、116 个动作块；374 个事件的首次命中／首次扫击开始均不变。365 个动作更早结束，9 个更晚结束，后者由原生最低结束时间规则造成。表中时间均为相对动作开始的秒数；结束时间是行为定时器，不是实测动画长度。连段的“首击后剩余”含后续攻击，不能称为纯后摇。

图形／物理及无关可选动作特性被替代；并非 374 次实机碰撞或动画录制测试。扫击列给出首次窗口开始，非最后窗口结束。攻击类型按原版每事件映射解析，包含纳垢兽等混合攻击类型配置。

边界实例：纳垢兽右侧甩尾的原始扫击窗口为 1.138889–1.527778 秒；1.4 倍率下行为在 1.405556 秒到期，早于原扫击窗口结束。原始窗口表没有整体缩放，这与完整动画／判定等比提速不同。

## chaos_armored_infected

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_armored_infected_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.287356 | 1.839080 | 1.554023 | -0.285057 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.264368 | 1.839080 | 1.531034 | -0.308046 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.609195 | 1.149425 | -0.459770 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.770115 | 1.264368 | -0.505747 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.609195 | 1.149425 | -0.459770 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.844444 | 1.911111 | 1.365079 | -0.546032 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.000000 | 1.844444 | 1.317460 | -0.526984 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.000000 | 2.000000 | 1.428571 | -0.571429 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 0.955556 | 1.733333 | 1.238095 | -0.495238 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.305556 | 2.388889 | 1.706349 | -0.682540 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.250000 | 2.222222 | 1.587302 | -0.634921 |

## chaos_beast_of_nurgle

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_beast_of_nurgle_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack_body_slam_aoe` / `attack_body_slam` | broadphase | 0.900000 | 1.566667 | 1.166667 | -0.400000 |
| `melee_attack_bwd` / `attack_tail_slam` | oobb | 0.818182 | 1.515152 | 1.084848 | -0.430303 |
| `melee_attack_fwd_left` / `attack_slam_left` | broadphase | 0.878788 | 1.696970 | 1.212121 | -0.484848 |
| `melee_attack_fwd_right` / `attack_slam_right` | broadphase | 0.969697 | 1.696970 | 1.236364 | -0.460606 |
| `melee_attack_left` / `attack_tail_whip_left` | sweep | 1.027778 | 1.944444 | 1.388889 | -0.555556 |
| `melee_attack_right` / `attack_tail_whip_right` | sweep | 1.138889 | 1.944444 | 1.405556 | -0.538889 |

## chaos_daemonhost

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_daemonhost_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `combo_attack` / `attack_combo` | oobb | 1.095238 | 2.857143 | 2.719048 | -0.138095 |
| `combo_attack` / `attack_combo_2` | oobb | 0.690476 | 2.142857 | 1.766667 | -0.376190 |
| `combo_attack` / `attack_combo_3` | oobb | 0.400000 | 3.133333 | 2.600000 | -0.533333 |
| `melee_attack` / `attack_down` | sweep | 0.466667 | 1.333333 | 0.952381 | -0.380952 |
| `melee_attack` / `attack_move_01` | sweep | 0.346667 | 0.986667 | 0.704762 | -0.281905 |
| `melee_attack` / `attack_move_02` | sweep | 0.346667 | 1.120000 | 0.800000 | -0.320000 |
| `melee_attack` / `attack_move_03` | sweep | 0.833333 | 1.400000 | 1.100000 | -0.300000 |
| `melee_attack` / `attack_up` | sweep | 0.666667 | 1.833333 | 1.309524 | -0.523810 |

## chaos_lesser_mutated_poxwalker

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_lesser_mutated_poxwalker_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.703704 | 2.740741 | 1.970370 | -0.770370 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.407407 | 2.320988 | 1.674074 | -0.646914 |
| `melee_attack` / `attack_03` | default_non_sweep | 1.259259 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_04` | default_non_sweep | 1.234568 | 2.617284 | 1.869489 | -0.747795 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.987654 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up_01` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 1.777778 | 2.962963 | 2.116402 | -0.846561 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.747126 | 2.804598 | 2.013793 | -0.790805 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.777778 | 2.987654 | 2.134039 | -0.853616 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 2.282051 | 3.256410 | 2.548718 | -0.707692 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.846154 | 2.538462 | 2.112821 | -0.425641 |

## chaos_mutated_poxwalker

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_mutated_poxwalker_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.703704 | 2.740741 | 1.970370 | -0.770370 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.407407 | 2.320988 | 1.674074 | -0.646914 |
| `melee_attack` / `attack_03` | default_non_sweep | 1.259259 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_04` | default_non_sweep | 1.234568 | 2.617284 | 1.869489 | -0.747795 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.987654 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up_01` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 1.777778 | 2.962963 | 2.116402 | -0.846561 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.747126 | 2.804598 | 2.013793 | -0.790805 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.777778 | 2.987654 | 2.134039 | -0.853616 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 2.282051 | 3.256410 | 2.548718 | -0.707692 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.846154 | 2.538462 | 2.112821 | -0.425641 |

## chaos_mutator_daemonhost

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_mutator_daemonhost_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `combo_attack` / `attack_combo` | oobb | 1.095238 | 2.857143 | 2.719048 | -0.138095 |
| `combo_attack` / `attack_combo_2` | oobb | 0.690476 | 2.142857 | 1.766667 | -0.376190 |
| `combo_attack` / `attack_combo_3` | oobb | 0.400000 | 3.133333 | 2.600000 | -0.533333 |
| `melee_attack` / `attack_down` | sweep | 0.466667 | 1.333333 | 0.952381 | -0.380952 |
| `melee_attack` / `attack_move_01` | sweep | 0.346667 | 0.986667 | 0.704762 | -0.281905 |
| `melee_attack` / `attack_move_02` | sweep | 0.346667 | 1.120000 | 0.800000 | -0.320000 |
| `melee_attack` / `attack_move_03` | sweep | 0.833333 | 1.400000 | 1.100000 | -0.300000 |
| `melee_attack` / `attack_up` | sweep | 0.666667 | 1.833333 | 1.309524 | -0.523810 |

## chaos_newly_infected

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_newly_infected_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.287356 | 1.839080 | 1.554023 | -0.285057 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.264368 | 1.839080 | 1.531034 | -0.308046 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.609195 | 1.149425 | -0.459770 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.770115 | 1.264368 | -0.505747 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.609195 | 1.149425 | -0.459770 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.844444 | 1.911111 | 1.365079 | -0.546032 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.000000 | 1.844444 | 1.317460 | -0.526984 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.000000 | 2.000000 | 1.428571 | -0.571429 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 0.955556 | 1.733333 | 1.238095 | -0.495238 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.305556 | 2.388889 | 1.706349 | -0.682540 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.250000 | 2.222222 | 1.587302 | -0.634921 |

## chaos_ogryn_bulwark

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_ogryn_bulwark_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | sweep | 0.909091 | 2.636364 | 1.883117 | -0.753247 |
| `melee_attack` / `attack_02` | sweep | 0.846154 | 2.179487 | 1.556777 | -0.622711 |
| `melee_attack` / `attack_03` | sweep | 1.466667 | 2.844444 | 2.031746 | -0.812698 |
| `melee_attack` / `attack_down_01` | sweep | 1.133333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | sweep | 1.060606 | 2.424242 | 1.731602 | -0.692641 |
| `shield_push` / `shield_push` | default_non_sweep | 0.466667 | 1.000000 | 0.733333 | -0.266667 |

## chaos_ogryn_executor

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_ogryn_executor_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_03` | default_non_sweep | 0.727273 | 1.848485 | 1.320346 | -0.528139 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.574713 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.620690 | 1.609195 | 1.149425 | -0.459770 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.505747 | 1.724138 | 1.231527 | -0.492611 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.066667 | 2.666667 | 1.904762 | -0.761905 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 0.692308 | 1.743590 | 1.245421 | -0.498168 |
| `melee_attack_cleave` / `attack_01` | oobb | 1.471264 | 3.103448 | 2.216749 | -0.886700 |
| `melee_attack_cleave` / `attack_02` | oobb | 1.310345 | 2.873563 | 2.052545 | -0.821018 |
| `melee_attack_cleave` / `attack_07` | oobb | 1.655172 | 3.678161 | 2.627258 | -1.050903 |
| `melee_attack_cleave` / `attack_08` | oobb | 1.586207 | 3.310345 | 2.364532 | -0.945813 |
| `melee_attack_kick` / `attack_push_kick_01` | default_non_sweep | 0.740741 | 1.975309 | 1.410935 | -0.564374 |
| `melee_attack_pommel` / `attack_pommel_01` | default_non_sweep | 0.493827 | 1.777778 | 1.269841 | -0.507937 |
| `melee_attack_punch` / `attack_push_punch_01` | default_non_sweep | 0.444444 | 1.358025 | 0.970018 | -0.388007 |
| `melee_attack_punch` / `attack_push_punch_02` | default_non_sweep | 0.518519 | 1.308642 | 0.934744 | -0.373898 |
| `melee_attack_punch` / `attack_push_punch_03` | default_non_sweep | 0.419753 | 1.481481 | 1.058201 | -0.423280 |
| `melee_attack_punch` / `attack_push_punch_04` | default_non_sweep | 0.567901 | 1.728395 | 1.234568 | -0.493827 |
| `melee_attack_punch` / `attack_push_punch_05` | default_non_sweep | 0.691358 | 1.679012 | 1.199295 | -0.479718 |
| `melee_attack_punch` / `attack_push_punch_06` | default_non_sweep | 0.694444 | 1.944444 | 1.388889 | -0.555556 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.333333 | 2.666667 | 1.904762 | -0.761905 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.055556 | 2.361111 | 1.686508 | -0.674603 |
| `moving_melee_attack_cleave` / `attack_move_01` | oobb | 1.530864 | 2.839506 | 2.028219 | -0.811287 |

## chaos_ogryn_gunner

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_ogryn_gunner_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.765432 | 2.469136 | 1.763668 | -0.705467 |
| `melee_attack` / `attack_push_punch_01` | default_non_sweep | 0.567901 | 1.975309 | 1.410935 | -0.564374 |
| `melee_attack_push` / `attack_push_01` | default_non_sweep | 0.691358 | 1.728395 | 1.234568 | -0.493827 |

## chaos_ogryn_houndmaster

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_ogryn_houndmaster_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `far_moving_attack` / `move_attack_06` | oobb | 1.212121 | 2.787879 | 2.387879 | -0.400000 |
| `far_moving_attack` / `move_attack_07` | oobb | 1.111111 | 2.555556 | 2.211111 | -0.344444 |
| `far_moving_attack` / `move_attack_09` | oobb | 1.066667 | 2.453333 | 2.133333 | -0.320000 |
| `melee_attack` / `attack_03` | oobb | 0.766667 | 1.500000 | 1.071429 | -0.428571 |
| `melee_attack` / `attack_04` | oobb | 0.833333 | 1.666667 | 1.190476 | -0.476190 |
| `melee_attack` / `attack_05` | oobb | 0.833333 | 1.500000 | 1.100000 | -0.400000 |
| `melee_attack` / `attack_06` | oobb | 1.000000 | 1.900000 | 1.357143 | -0.542857 |
| `melee_attack` / `attack_down_01` | oobb | 1.066667 | 2.666667 | 1.904762 | -0.761905 |
| `melee_attack` / `attack_reach_up` | oobb | 0.900000 | 2.266667 | 1.619048 | -0.647619 |
| `melee_attack` / `attack_standing_combo` | oobb | 0.700000 | 2.300000 | 1.966667 | -0.333333 |
| `moving_melee_attack_cleave` / `move_attack_cleave` | oobb | 1.111111 | 2.416667 | 1.726190 | -0.690476 |
| `moving_melee_attack_cleave` / `move_attack_cleave_02` | oobb | 1.527778 | 2.500000 | 1.794444 | -0.705556 |
| `moving_melee_attack_cleave` / `move_attack_cleave_03` | oobb | 0.888889 | 1.861111 | 1.329365 | -0.531746 |
| `moving_melee_attack_cleave` / `move_attack_cleave_04` | oobb | 1.000000 | 1.666667 | 1.266667 | -0.400000 |

## chaos_plague_ogryn

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_plague_ogryn_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `catapult_attack` / `attack_catapult` | oobb | 0.825397 | 2.285714 | 1.632653 | -0.653061 |
| `combo_attack` / `attack_sword_combo` | sweep | 1.096296 | 3.555556 | 2.539683 | -1.015873 |
| `melee_slam` / `attack_reach_up` | oobb | 0.966667 | 2.333333 | 1.666667 | -0.666667 |
| `melee_slam` / `attack_slam` | oobb | 0.651852 | 1.777778 | 1.269841 | -0.507937 |
| `plague_stomp` / `attack_stomp` | broadphase | 1.060606 | 1.969697 | 1.406926 | -0.562771 |

## chaos_poxwalker

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_poxwalker_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.703704 | 2.740741 | 1.970370 | -0.770370 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.407407 | 2.320988 | 1.674074 | -0.646914 |
| `melee_attack` / `attack_03` | default_non_sweep | 1.259259 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_04` | default_non_sweep | 1.234568 | 2.617284 | 1.869489 | -0.747795 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.987654 | 2.246914 | 1.604938 | -0.641975 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up_01` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 1.777778 | 2.962963 | 2.116402 | -0.846561 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.747126 | 2.804598 | 2.013793 | -0.790805 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.777778 | 2.987654 | 2.134039 | -0.853616 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 2.282051 | 3.256410 | 2.548718 | -0.707692 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.846154 | 2.538462 | 2.112821 | -0.425641 |

## chaos_spawn

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/chaos/chaos_spawn_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `change_target_combo` / `attack_melee_combo` | sweep | 0.433333 | 2.166667 | 1.547619 | -0.619048 |
| `change_target_combo` / `attack_melee_combo_2` | sweep | 0.444444 | 2.000000 | 1.428571 | -0.571429 |
| `change_target_combo` / `attack_melee_combo_3` | sweep | 0.600000 | 2.400000 | 1.714286 | -0.685714 |
| `change_target_combo` / `attack_melee_combo_4` | sweep | 1.000000 | 2.500000 | 1.785714 | -0.714286 |
| `change_target_combo` / `attack_turn_bwd` | sweep | 0.666667 | 2.333333 | 1.666667 | -0.666667 |
| `change_target_combo` / `attack_turn_left` | sweep | 0.566667 | 2.333333 | 1.666667 | -0.666667 |
| `change_target_combo` / `attack_turn_right` | sweep | 0.566667 | 2.000000 | 1.428571 | -0.571429 |
| `claw_attack` / `attack_melee_claw` | oobb | 0.666667 | 1.166667 | 0.933333 | -0.233333 |
| `claw_attack` / `attack_melee_claw_02` | oobb | 0.666667 | 1.166667 | 0.933333 | -0.233333 |
| `combo_attack` / `attack_melee_combo` | sweep | 0.433333 | 2.166667 | 1.547619 | -0.619048 |
| `combo_attack` / `attack_melee_combo_2` | sweep | 0.444444 | 2.000000 | 1.428571 | -0.571429 |
| `combo_attack` / `attack_melee_combo_3` | sweep | 0.600000 | 2.400000 | 1.714286 | -0.685714 |
| `combo_attack` / `attack_melee_combo_4` | sweep | 1.000000 | 2.500000 | 1.785714 | -0.714286 |
| `combo_attack` / `attack_turn_bwd` | sweep | 0.666667 | 2.333333 | 1.666667 | -0.666667 |
| `combo_attack` / `attack_turn_left` | sweep | 0.566667 | 2.333333 | 1.666667 | -0.666667 |
| `combo_attack` / `attack_turn_right` | sweep | 0.566667 | 2.000000 | 1.428571 | -0.571429 |

## cultist_assault

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_assault_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |

## cultist_berzerker

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_berzerker_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `combo_attack` / `attack_move_combo_01_fast` | default_non_sweep | 0.666667 | 3.333333 | 3.219048 | -0.114286 |
| `combo_attack` / `attack_move_combo_08_fast` | default_non_sweep | 0.500000 | 3.055556 | 3.155556 | +0.100000 |
| `leap_attack` / `attack_move_combo_04_fast` | default_non_sweep | 0.472222 | 2.722222 | 2.850000 | +0.127778 |
| `melee_attack` / `attack_01` | default_non_sweep | 0.433333 | 0.933333 | 0.700000 | -0.233333 |
| `melee_attack` / `attack_02` | default_non_sweep | 0.466667 | 0.933333 | 0.733333 | -0.200000 |
| `melee_attack` / `attack_03` | default_non_sweep | 0.466667 | 0.933333 | 0.733333 | -0.200000 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.566667 | 1.000000 | 0.833333 | -0.166667 |
| `melee_attack` / `attack_combo_standing_06` | default_non_sweep | 0.466667 | 1.266667 | 1.233333 | -0.033333 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 0.700000 | 2.100000 | 1.500000 | -0.600000 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 0.766667 | 1.666667 | 1.190476 | -0.476190 |

## cultist_captain

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_captain_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `kick` / `attack_kick_01` | oobb | 0.666667 | 1.733333 | 1.238095 | -0.495238 |
| `kick` / `attack_kick_02` | oobb | 0.426667 | 1.226667 | 0.876190 | -0.350476 |
| `kick` / `attack_knee_01` | oobb | 0.613333 | 1.680000 | 1.200000 | -0.480000 |
| `power_sword_melee_attack` / `attack_04` | default_non_sweep | 0.645833 | 1.250000 | 0.912500 | -0.337500 |
| `power_sword_melee_attack` / `attack_05` | default_non_sweep | 0.687500 | 1.395833 | 0.997024 | -0.398810 |
| `power_sword_melee_attack` / `attack_06` | default_non_sweep | 0.645833 | 1.250000 | 0.912500 | -0.337500 |
| `power_sword_melee_attack` / `attack_07` | default_non_sweep | 0.645833 | 1.333333 | 0.952381 | -0.380952 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_01` | oobb | 0.623656 | 2.400000 | 2.137634 | -0.262366 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_02` | oobb | 0.602151 | 3.466667 | 2.696774 | -0.769892 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_03` | oobb | 0.602151 | 2.853333 | 2.546237 | -0.307097 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_04` | oobb | 0.559140 | 2.666667 | 2.395699 | -0.270968 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_05` | oobb | 0.537634 | 2.800000 | 2.417204 | -0.382796 |
| `power_sword_melee_sweep` / `attack_heavy_swing` | sweep | 2.166667 | 3.333333 | 2.433333 | -0.900000 |
| `power_sword_moving_melee_attack` / `attack_move_01` | oobb | 0.938272 | 1.728395 | 1.234568 | -0.493827 |
| `power_sword_moving_melee_attack` / `attack_move_02` | oobb | 1.111111 | 1.728395 | 1.377778 | -0.350617 |
| `power_sword_moving_melee_attack` / `attack_move_03` | oobb | 1.111111 | 1.728395 | 1.377778 | -0.350617 |
| `power_sword_moving_melee_attack` / `attack_move_04` | oobb | 1.061728 | 1.728395 | 1.328395 | -0.400000 |
| `powermaul_ground_slam` / `cultist_heavy_slam` | oobb | 1.488889 | 3.000000 | 2.142857 | -0.857143 |
| `powermaul_melee_attack` / `cultist_captain_heavy` | default_non_sweep | 1.100000 | 2.000000 | 1.428571 | -0.571429 |
| `powermaul_melee_cleave` / `attack_01` | oobb | 1.517241 | 3.103448 | 2.216749 | -0.886700 |
| `powermaul_melee_cleave` / `attack_02` | oobb | 1.310345 | 2.873563 | 2.052545 | -0.821018 |
| `powermaul_moving_melee_cleave` / `attack_move_01` | oobb | 1.481481 | 2.839506 | 2.028219 | -0.811287 |
| `powermaul_pommel` / `attack_2h_pommel` | oobb | 0.733333 | 1.600000 | 1.142857 | -0.457143 |
| `punch` / `attack_pommel_01` | oobb | 0.543210 | 1.358025 | 0.970018 | -0.388007 |
| `punch` / `attack_pommel_02` | oobb | 0.716049 | 1.604938 | 1.146384 | -0.458554 |
| `punch` / `attack_pommel_03` | oobb | 0.814815 | 1.851852 | 1.322751 | -0.529101 |

## cultist_flamer

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_flamer_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.395062 | 1.111111 | 0.793651 | -0.317460 |

## cultist_grenadier

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_grenadier_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_kick_01` | default_non_sweep | 0.694444 | 1.555556 | 1.111111 | -0.444444 |
| `melee_attack` / `attack_kick_02` | default_non_sweep | 0.444444 | 1.055556 | 0.753968 | -0.301587 |

## cultist_gunner

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_gunner_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `bayonet_melee_attack` / `attack_bayonet_01` | default_non_sweep | 0.574713 | 1.444444 | 1.031746 | -0.412698 |
| `bayonet_melee_attack` / `attack_bayonet_02` | default_non_sweep | 0.758621 | 2.068966 | 1.477833 | -0.591133 |
| `bayonet_melee_attack` / `attack_bayonet_04` | default_non_sweep | 1.222222 | 2.222222 | 1.587302 | -0.634921 |
| `bayonet_melee_attack` / `attack_bayonet_05` | default_non_sweep | 1.333333 | 2.600000 | 1.857143 | -0.742857 |

## cultist_melee

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_melee_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 0.733333 | 2.000000 | 1.428571 | -0.571429 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.566667 | 2.866667 | 2.047619 | -0.819048 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.500000 | 2.666667 | 1.904762 | -0.761905 |

## cultist_shocktrooper

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_shocktrooper_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `bayonet_charge_attack` / `bayonet_charge_hit` | default_non_sweep | 0.466667 | 2.166667 | 1.547619 | -0.619048 |
| `bayonet_charge_attack` / `bayonet_charge_hit_02` | default_non_sweep | 0.722222 | 1.666667 | 1.190476 | -0.476190 |
| `bayonet_charge_attack` / `bayonet_charge_hit_03` | default_non_sweep | 0.666667 | 1.611111 | 1.150794 | -0.460317 |
| `bayonet_charge_attack` / `bayonet_charge_hit_04` | default_non_sweep | 1.388889 | 2.500000 | 1.785714 | -0.714286 |
| `bayonet_charge_attack` / `bayonet_charge_hit_05` | default_non_sweep | 1.222222 | 2.361111 | 1.686508 | -0.674603 |
| `bayonet_melee_attack` / `attack_bayonet_01` | default_non_sweep | 0.574713 | 1.444444 | 1.031746 | -0.412698 |
| `bayonet_melee_attack` / `attack_bayonet_02` | default_non_sweep | 0.758621 | 2.068966 | 1.477833 | -0.591133 |
| `bayonet_melee_attack` / `attack_bayonet_04` | default_non_sweep | 1.222222 | 2.222222 | 1.587302 | -0.634921 |
| `bayonet_melee_attack` / `attack_bayonet_05` | default_non_sweep | 1.333333 | 2.600000 | 1.857143 | -0.742857 |

## cultist_vanguard

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/cultist/cultist_vanguard_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.594203 | 2.608696 | 1.863354 | -0.745342 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.594203 | 2.608696 | 1.863354 | -0.745342 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.898551 | 1.739130 | 1.242236 | -0.496894 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.333333 | 3.043478 | 2.173913 | -0.869565 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 1.101449 | 2.492754 | 1.780538 | -0.712215 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.304348 | 2.405797 | 1.718427 | -0.687371 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.304348 | 2.608696 | 1.863354 | -0.745342 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.246377 | 2.260870 | 1.614907 | -0.645963 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 0.733333 | 2.000000 | 1.428571 | -0.571429 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.566667 | 2.866667 | 2.047619 | -0.819048 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.500000 | 2.666667 | 1.904762 | -0.761905 |

## renegade_assault

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_assault_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |

## renegade_berzerker

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_berzerker_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `combo_attack` / `attack_combo_01` | default_non_sweep | 0.746667 | 3.733333 | 3.573333 | -0.160000 |
| `combo_attack` / `attack_combo_04` | default_non_sweep | 0.566667 | 3.266667 | 3.366667 | +0.100000 |
| `combo_attack` / `attack_combo_08` | default_non_sweep | 0.600000 | 3.666667 | 3.733333 | +0.066667 |
| `melee_attack` / `attack_01` | default_non_sweep | 0.433333 | 1.166667 | 0.833333 | -0.333333 |
| `melee_attack` / `attack_02` | default_non_sweep | 0.466667 | 1.166667 | 0.833333 | -0.333333 |
| `melee_attack` / `attack_03` | default_non_sweep | 0.466667 | 1.166667 | 0.833333 | -0.333333 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.566667 | 1.333333 | 0.952381 | -0.380952 |
| `melee_attack` / `attack_combo_standing_06` | default_non_sweep | 0.466667 | 1.500000 | 1.233333 | -0.266667 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 0.700000 | 2.100000 | 1.500000 | -0.600000 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 0.766667 | 1.666667 | 1.190476 | -0.476190 |

## renegade_captain

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_captain_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `kick` / `attack_kick_01` | oobb | 0.666667 | 1.733333 | 1.238095 | -0.495238 |
| `kick` / `attack_kick_02` | oobb | 0.426667 | 1.226667 | 0.876190 | -0.350476 |
| `kick` / `attack_knee_01` | oobb | 0.613333 | 1.680000 | 1.200000 | -0.480000 |
| `power_sword_melee_attack` / `attack_04` | default_non_sweep | 0.645833 | 1.250000 | 0.912500 | -0.337500 |
| `power_sword_melee_attack` / `attack_05` | default_non_sweep | 0.687500 | 1.395833 | 0.997024 | -0.398810 |
| `power_sword_melee_attack` / `attack_06` | default_non_sweep | 0.645833 | 1.250000 | 0.912500 | -0.337500 |
| `power_sword_melee_attack` / `attack_07` | default_non_sweep | 0.645833 | 1.333333 | 0.952381 | -0.380952 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_02` | oobb | 0.602151 | 3.466667 | 2.696774 | -0.769892 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_03` | oobb | 0.602151 | 2.853333 | 2.546237 | -0.307097 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_04` | oobb | 0.559140 | 2.666667 | 2.395699 | -0.270968 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_05` | oobb | 0.537634 | 2.800000 | 2.417204 | -0.382796 |
| `power_sword_melee_sweep` / `attack_heavy_swing` | sweep | 2.166667 | 3.333333 | 2.433333 | -0.900000 |
| `power_sword_moving_melee_attack` / `attack_move_01` | oobb | 0.938272 | 1.728395 | 1.234568 | -0.493827 |
| `power_sword_moving_melee_attack` / `attack_move_02` | oobb | 1.111111 | 1.728395 | 1.377778 | -0.350617 |
| `power_sword_moving_melee_attack` / `attack_move_03` | oobb | 1.111111 | 1.728395 | 1.377778 | -0.350617 |
| `power_sword_moving_melee_attack` / `attack_move_04` | oobb | 1.061728 | 1.728395 | 1.328395 | -0.400000 |
| `powermaul_ground_slam` / `attack_ground_slam` | oobb | 2.233333 | 4.500000 | 3.214286 | -1.285714 |
| `powermaul_melee_attack` / `attack_03` | default_non_sweep | 0.459770 | 2.298851 | 1.642036 | -0.656814 |
| `powermaul_melee_attack` / `attack_04` | default_non_sweep | 0.617284 | 1.901235 | 1.358025 | -0.543210 |
| `powermaul_melee_cleave` / `attack_01` | oobb | 1.517241 | 3.103448 | 2.216749 | -0.886700 |
| `powermaul_melee_cleave` / `attack_02` | oobb | 1.310345 | 2.873563 | 2.052545 | -0.821018 |
| `powermaul_moving_melee_cleave` / `attack_move_01` | oobb | 1.481481 | 2.839506 | 2.028219 | -0.811287 |
| `powermaul_pommel` / `attack_2h_pommel` | oobb | 0.733333 | 1.600000 | 1.142857 | -0.457143 |
| `punch` / `attack_pommel_01` | oobb | 0.543210 | 1.358025 | 0.970018 | -0.388007 |
| `punch` / `attack_pommel_02` | oobb | 0.716049 | 1.604938 | 1.146384 | -0.458554 |
| `punch` / `attack_pommel_03` | oobb | 0.814815 | 1.851852 | 1.322751 | -0.529101 |

## renegade_executor

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_executor_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_03` | default_non_sweep | 0.613333 | 1.733333 | 1.238095 | -0.495238 |
| `melee_attack` / `attack_04` | default_non_sweep | 0.693333 | 1.466667 | 1.047619 | -0.419048 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 2.166667 | 4.500000 | 3.214286 | -1.285714 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 0.692308 | 1.743590 | 1.245421 | -0.498168 |
| `melee_cleave_attack` / `attack_01` | default_non_sweep | 1.471264 | 2.436782 | 1.740558 | -0.696223 |
| `melee_cleave_attack` / `attack_02` | default_non_sweep | 1.241379 | 2.068966 | 1.508046 | -0.560920 |
| `melee_cleave_attack` / `attack_down_01` | default_non_sweep | 2.166667 | 4.500000 | 3.214286 | -1.285714 |
| `melee_cleave_attack` / `attack_reach_up` | default_non_sweep | 0.692308 | 1.743590 | 1.245421 | -0.498168 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.185185 | 2.370370 | 1.693122 | -0.677249 |
| `moving_melee_cleave_attack` / `attack_move_01` | default_non_sweep | 1.481481 | 2.839506 | 2.028219 | -0.811287 |

## renegade_flamer

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_flamer_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.395062 | 1.111111 | 0.793651 | -0.317460 |

## renegade_flamer_mutator

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_flamer_mutator_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.395062 | 1.111111 | 0.793651 | -0.317460 |

## renegade_grenadier

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_grenadier_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_kick_01` | default_non_sweep | 0.694444 | 1.555556 | 1.111111 | -0.444444 |
| `melee_attack` / `attack_kick_02` | default_non_sweep | 0.444444 | 1.055556 | 0.753968 | -0.301587 |

## renegade_gunner

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_gunner_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_pommel_01` | default_non_sweep | 0.518519 | 1.728395 | 1.234568 | -0.493827 |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.765432 | 2.469136 | 1.763668 | -0.705467 |

## renegade_melee

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_melee_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 0.733333 | 2.000000 | 1.428571 | -0.571429 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.566667 | 2.866667 | 2.047619 | -0.819048 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.500000 | 2.666667 | 1.904762 | -0.761905 |

## renegade_plasma_gunner

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_plasma_gunner_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |

## renegade_radio_operator

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_radio_operator_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_pommel_01` | default_non_sweep | 0.518519 | 1.728395 | 1.234568 | -0.493827 |
| `melee_attack` / `attack_push_kick_01` | default_non_sweep | 0.765432 | 2.469136 | 1.763668 | -0.705467 |

## renegade_rifleman

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_rifleman_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `bayonet_charge_attack` / `bayonet_charge_hit` | default_non_sweep | 0.466667 | 2.166667 | 1.547619 | -0.619048 |
| `bayonet_charge_attack` / `bayonet_charge_hit_02` | default_non_sweep | 0.722222 | 1.666667 | 1.190476 | -0.476190 |
| `bayonet_charge_attack` / `bayonet_charge_hit_03` | default_non_sweep | 0.666667 | 1.611111 | 1.150794 | -0.460317 |
| `bayonet_charge_attack` / `bayonet_charge_hit_04` | default_non_sweep | 1.388889 | 2.500000 | 1.785714 | -0.714286 |
| `bayonet_charge_attack` / `bayonet_charge_hit_05` | default_non_sweep | 1.222222 | 2.361111 | 1.686508 | -0.674603 |
| `melee_attack` / `bayonet_attack_stab` | default_non_sweep | 0.488889 | 1.444444 | 1.031746 | -0.412698 |
| `melee_attack` / `bayonet_attack_stab_02` | default_non_sweep | 1.222222 | 2.222222 | 1.587302 | -0.634921 |
| `melee_attack` / `bayonet_attack_sweep` | default_non_sweep | 0.689655 | 2.068966 | 1.477833 | -0.591133 |
| `melee_attack` / `bayonet_attack_sweep_02` | default_non_sweep | 1.400000 | 2.833333 | 2.023810 | -0.809524 |

## renegade_shocktrooper

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_shocktrooper_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_04` | default_non_sweep | 0.765432 | 1.379310 | 1.032099 | -0.347212 |
| `melee_attack` / `attack_05` | default_non_sweep | 0.814815 | 1.540230 | 1.100164 | -0.440066 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.712644 | 1.379310 | 0.985222 | -0.394089 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.179487 | 2.692308 | 1.923077 | -0.769231 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 0.938272 | 2.123457 | 1.516755 | -0.606702 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.111111 | 2.049383 | 1.463845 | -0.585538 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.111111 | 2.222222 | 1.587302 | -0.634921 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.061728 | 1.925926 | 1.375661 | -0.550265 |

## renegade_sniper

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_sniper_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_kick_01` | default_non_sweep | 0.666667 | 1.733333 | 1.238095 | -0.495238 |
| `melee_attack` / `attack_pommel_01` | default_non_sweep | 0.518519 | 1.728395 | 1.234568 | -0.493827 |

## renegade_twin_captain

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_twin_captain_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `kick` / `attack_kick_01` | oobb | 0.666667 | 1.200000 | 0.933333 | -0.266667 |
| `kick` / `attack_kick_02` | oobb | 0.426667 | 0.666667 | 0.693333 | +0.026667 |

## renegade_twin_captain_two

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_twin_captain_two_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `kick` / `attack_kick_01` | oobb | 0.666667 | 1.200000 | 0.933333 | -0.266667 |
| `kick` / `attack_kick_02` | oobb | 0.426667 | 0.666667 | 0.693333 | +0.026667 |
| `kick` / `attack_knee_01` | oobb | 0.613333 | 1.200000 | 0.880000 | -0.320000 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_01` | oobb | 0.623656 | 2.150538 | 2.137634 | -0.012903 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_02` | oobb | 0.602151 | 2.795699 | 2.696774 | -0.098925 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_03` | oobb | 0.602151 | 2.301075 | 2.546237 | +0.245161 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_04` | oobb | 0.559140 | 2.365591 | 2.395699 | +0.030108 |
| `power_sword_melee_combo_attack` / `attack_swing_combo_05` | oobb | 0.537634 | 2.258065 | 2.417204 | +0.159140 |
| `power_sword_melee_sweep` / `attack_heavy_swing_fast` | sweep | 0.833333 | 1.666667 | 1.190476 | -0.476190 |
| `power_sword_melee_sweep` / `attack_heavy_swing_fast_02` | sweep | 1.354167 | 1.666667 | 1.620833 | -0.045833 |
| `power_sword_moving_melee_sweep` / `attack_heavy_swing_moving` | sweep | 1.466667 | 2.500000 | 1.785714 | -0.714286 |

## renegade_vanguard

[原版动作数据](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breed_actions/renegade/renegade_vanguard_actions.lua#L1)

| 动作块／事件 | 类型 | 首击／扫击开始（均不变） | 原结束 | 1.4 结束 | 结束变化 |
| --- | --- | ---: | ---: | ---: | ---: |
| `melee_attack` / `attack_01` | default_non_sweep | 1.594203 | 2.608696 | 1.863354 | -0.745342 |
| `melee_attack` / `attack_02` | default_non_sweep | 1.594203 | 2.608696 | 1.863354 | -0.745342 |
| `melee_attack` / `attack_06` | default_non_sweep | 0.898551 | 1.739130 | 1.242236 | -0.496894 |
| `melee_attack` / `attack_07` | default_non_sweep | 0.700000 | 1.833333 | 1.309524 | -0.523810 |
| `melee_attack` / `attack_down_01` | default_non_sweep | 1.333333 | 3.333333 | 2.380952 | -0.952381 |
| `melee_attack` / `attack_reach_up` | default_non_sweep | 1.333333 | 3.043478 | 2.173913 | -0.869565 |
| `moving_melee_attack` / `attack_move_01` | default_non_sweep | 1.101449 | 2.492754 | 1.780538 | -0.712215 |
| `moving_melee_attack` / `attack_move_02` | default_non_sweep | 1.304348 | 2.405797 | 1.718427 | -0.687371 |
| `moving_melee_attack` / `attack_move_03` | default_non_sweep | 1.304348 | 2.608696 | 1.863354 | -0.745342 |
| `moving_melee_attack` / `attack_move_04` | default_non_sweep | 1.246377 | 2.260870 | 1.614907 | -0.645963 |
| `running_melee_attack` / `attack_run_01` | default_non_sweep | 0.733333 | 2.000000 | 1.428571 | -0.571429 |
| `running_melee_attack` / `attack_run_02` | default_non_sweep | 1.566667 | 2.866667 | 2.047619 | -0.819048 |
| `running_melee_attack` / `attack_run_03` | default_non_sweep | 1.500000 | 2.666667 | 1.904762 | -0.761905 |

