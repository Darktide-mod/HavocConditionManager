# 敌人速度接口完整目录

固定原版提交 `0f0cb45991e9305ef4a7b925370792d7d6035f95`。主报告：[红针、毒气和各类速度接口的解释](<F:/SteamLibrary/steamapps/common/Warhammer 40,000 DARKTIDE/mod-work/havoc-redesign-20260905/projects/HavocConditionManager/docs/Enemy-speed-stim-gas-audit-20260912.zh-CN.md>)。

共 49 份品种定义、50 棵敌人目录下的行为树；后者含 2 棵 TG 测试树。行为树引用了动作目录中的 77 个实现。表中的“移速初始化”只表示满足普通近战追击保留正向移速倍率的必要条件，不代表所有动作都能加速。

品种名称保留原始标识，避免混淆本地化名称与变体。`chaos_hound_mutator` 的定义内部 breed_name 仍为 chaos_hound，因此不能按内部名字去重；变种人变体复用普通变种人的行为树。

## 品种与真实动作映射

| 品种定义 | 行为树 | 移速初始化 | 普通近战动作名 | 使用共享开火／连射的动作类 |
| --- | --- | --- | --- | --- |
| [chaos_armored_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_armored_hound_breed.lua#L1) | [chaos_armored_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_armored_hound_behavior_tree.lua#L1) | 无 | — | — |
| [chaos_armored_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_armored_infected_breed.lua#L1) | [chaos_armored_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_armored_infected_behavior_tree.lua#L1) | 有 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [chaos_beast_of_nurgle](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_beast_of_nurgle_breed.lua#L1) | [chaos_beast_of_nurgle](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_beast_of_nurgle_behavior_tree.lua#L1) | 无 | `melee_attack_body_slam_aoe`、`melee_attack_bwd`、`melee_attack_fwd_left`、`melee_attack_fwd_right`、`melee_attack_left`、`melee_attack_right` | — |
| [chaos_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_daemonhost_breed.lua#L1) | [chaos_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_daemonhost_behavior_tree.lua#L1) | 无 | `combo_attack`、`melee_attack` | — |
| [chaos_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_hound_breed.lua#L1) | [chaos_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_hound_behavior_tree.lua#L1) | 无 | — | — |
| [chaos_hound_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_hound_mutator_breed.lua#L1) | [chaos_hound_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_hound_mutator_behavior_tree.lua#L1) | 无 | — | — |
| [chaos_lesser_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_lesser_mutated_poxwalker_breed.lua#L1) | [chaos_lesser_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_lesser_mutated_poxwalker_behavior_tree.lua#L1) | 有 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [chaos_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutated_poxwalker_breed.lua#L1) | [chaos_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutated_poxwalker_behavior_tree.lua#L1) | 有 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [chaos_mutator_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutator_daemonhost_breed.lua#L1) | [chaos_mutator_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutator_daemonhost_behavior_tree.lua#L1) | 无 | `combo_attack`、`melee_attack` | — |
| [chaos_mutator_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutator_ritualist_breed.lua#L1) | [chaos_mutator_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutator_ritualist_behavior_tree.lua#L1) | 无 | — | — |
| [chaos_newly_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_newly_infected_breed.lua#L1) | [chaos_newly_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_newly_infected_behavior_tree.lua#L1) | 有 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [chaos_ogryn_bulwark](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_bulwark_breed.lua#L1) | [chaos_ogryn_bulwark](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_bulwark_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack`、`shield_push` | — |
| [chaos_ogryn_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_executor_breed.lua#L1) | [chaos_ogryn_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_executor_behavior_tree.lua#L1) | 无 | `melee_attack`、`melee_attack_cleave`、`melee_attack_kick`、`melee_attack_pommel`、`melee_attack_punch`、`moving_melee_attack`、`moving_melee_attack_cleave` | — |
| [chaos_ogryn_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_gunner_breed.lua#L1) | [chaos_ogryn_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_gunner_behavior_tree.lua#L1) | 无 | `melee_attack`、`melee_attack_push` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [chaos_ogryn_houndmaster](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_houndmaster_breed.lua#L1) | [chaos_ogryn_houndmaster](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_houndmaster_behavior_tree.lua#L1) | 有 | `far_moving_attack`、`melee_attack`、`moving_melee_attack_cleave` | — |
| [chaos_plague_ogryn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_plague_ogryn_breed.lua#L1) | [chaos_plague_ogryn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_plague_ogryn_behavior_tree.lua#L1) | 无 | `catapult_attack`、`combo_attack`、`melee_slam`、`plague_stomp` | — |
| [chaos_poxwalker_bomber](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_poxwalker_bomber_breed.lua#L1) | [chaos_poxwalker_bomber](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_poxwalker_bomber_behavior_tree.lua#L1) | 无 | — | — |
| [chaos_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_poxwalker_breed.lua#L1) | [chaos_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_poxwalker_behavior_tree.lua#L1) | 有 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [chaos_spawn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_spawn_breed.lua#L1) | [chaos_spawn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_spawn_behavior_tree.lua#L1) | 无 | `change_target_combo`、`claw_attack`、`combo_attack` | — |
| [cultist_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_assault_breed.lua#L1) | [cultist_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_assault_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)、[BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [cultist_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_berzerker_breed.lua#L1) | [cultist_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_berzerker_behavior_tree.lua#L1) | 有 | `combo_attack`、`leap_attack`、`melee_attack` | — |
| [cultist_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_captain_breed.lua#L1) | [cultist_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_captain_behavior_tree.lua#L1) | 无 | `kick`、`power_sword_melee_attack`、`power_sword_melee_combo_attack`、`power_sword_melee_sweep`、`power_sword_moving_melee_attack`、`powermaul_ground_slam`、`powermaul_melee_attack`、`powermaul_melee_cleave`、`powermaul_moving_melee_cleave`、`powermaul_pommel`、`punch` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [cultist_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_flamer_breed.lua#L1) | [cultist_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_flamer_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [cultist_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_grenadier_breed.lua#L1) | [cultist_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_grenadier_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [cultist_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_gunner_breed.lua#L1) | [cultist_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_gunner_behavior_tree.lua#L1) | 无 | `bayonet_melee_attack` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [cultist_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_melee_breed.lua#L1) | [cultist_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_melee_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_mutant_breed.lua#L1) | [cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_mutant_behavior_tree.lua#L1) | 无 | — | — |
| [cultist_mutant_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_mutant_mutator_breed.lua#L1) | [cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_mutant_behavior_tree.lua#L1) | 无 | — | — |
| [cultist_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_ritualist_breed.lua#L1) | [cultist_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_ritualist_behavior_tree.lua#L1) | 无 | — | — |
| [cultist_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_shocktrooper_breed.lua#L1) | [cultist_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_shocktrooper_behavior_tree.lua#L1) | 无 | `bayonet_charge_attack`、`bayonet_melee_attack` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1)、[BtStepShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L1) |
| [cultist_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_vanguard_breed.lua#L1) | [cultist_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_vanguard_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [renegade_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_assault_breed.lua#L1) | [renegade_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_assault_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_berzerker_breed.lua#L1) | [renegade_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_berzerker_behavior_tree.lua#L1) | 有 | `combo_attack`、`melee_attack` | — |
| [renegade_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_captain_breed.lua#L1) | [renegade_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_captain_behavior_tree.lua#L1) | 无 | `kick`、`power_sword_melee_attack`、`power_sword_melee_combo_attack`、`power_sword_melee_sweep`、`power_sword_moving_melee_attack`、`powermaul_ground_slam`、`powermaul_melee_attack`、`powermaul_melee_cleave`、`powermaul_moving_melee_cleave`、`powermaul_pommel`、`punch` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_executor_breed.lua#L1) | [renegade_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_executor_behavior_tree.lua#L1) | 无 | `melee_attack`、`melee_cleave_attack`、`moving_melee_attack`、`moving_melee_cleave_attack` | — |
| [renegade_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_flamer_breed.lua#L1) | [renegade_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_flamer_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [renegade_flamer_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_flamer_mutator_breed.lua#L1) | [renegade_flamer_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_flamer_mutator_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [renegade_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_grenadier_breed.lua#L1) | [renegade_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_grenadier_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [renegade_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_gunner_breed.lua#L1) | [renegade_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_gunner_behavior_tree.lua#L1) | 无 | `melee_attack` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_melee_breed.lua#L1) | [renegade_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_melee_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |
| [renegade_netgunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_netgunner_breed.lua#L1) | [renegade_netgunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_netgunner_behavior_tree.lua#L1) | 无 | — | — |
| [renegade_plasma_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_plasma_gunner_breed.lua#L1) | [renegade_plasma_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_plasma_gunner_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_radio_operator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_radio_operator_breed.lua#L1) | [renegade_radio_operator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_radio_operator_behavior_tree.lua#L1) | 无 | `melee_attack` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_rifleman](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_rifleman_breed.lua#L1) | [renegade_rifleman](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_rifleman_behavior_tree.lua#L1) | 无 | `bayonet_charge_attack`、`melee_attack` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_shocktrooper_breed.lua#L1) | [renegade_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_shocktrooper_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1)、[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1)、[BtStepShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L1) |
| [renegade_sniper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_sniper_breed.lua#L1) | [renegade_sniper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_sniper_behavior_tree.lua#L1) | 无 | `melee_attack` | — |
| [renegade_twin_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_twin_captain_breed.lua#L1) | [renegade_twin_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_twin_captain_behavior_tree.lua#L1) | 无 | `kick` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) |
| [renegade_twin_captain_two](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_twin_captain_two_breed.lua#L1) | [renegade_twin_captain_two](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_twin_captain_two_behavior_tree.lua#L1) | 无 | `kick`、`power_sword_melee_combo_attack`、`power_sword_melee_sweep`、`power_sword_moving_melee_sweep` | — |
| [renegade_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_vanguard_breed.lua#L1) | [renegade_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_vanguard_behavior_tree.lua#L1) | 无 | `melee_attack`、`moving_melee_attack`、`running_melee_attack` | — |

## 每份品种定义的行为节点

按实际行为树展开动作节点，保留同一动作类的不同事件／数据入口。选择器不列入下面的动作表；条件与完整树结构可通过源码链接查询。

### chaos_armored_hound

定义：[chaos_armored_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_armored_hound_breed.lua#L1)；行为树：[chaos_armored_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_armored_hound_behavior_tree.lua#L1)。

声明的动画变量：`gallop_lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_armored_hound.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_armored_hound.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_armored_hound.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_armored_hound.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_armored_hound.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_armored_hound.stagger` |
| `approach_target` | [BtChaosHoundApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L1) | `chaos_armored_hound.approach_target` |
| `leap` | [BtChaosHoundLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L1) | `chaos_armored_hound.leap` |
| `target_pounced` | [BtChaosHoundTargetPouncedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L1) | `chaos_armored_hound.target_pounced` |
| `skulking` | [BtChaosHoundSkulkAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L1) | `chaos_armored_hound.skulking` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_armored_hound.patrol` |
| `roaming` | [BtChaosHoundRoamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L1) | `chaos_armored_hound.roaming` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_armored_hound.idle` |

### chaos_armored_infected

定义：[chaos_armored_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_armored_infected_breed.lua#L1)；行为树：[chaos_armored_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_armored_infected_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_armored_infected.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_armored_infected.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_armored_infected.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_armored_infected.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_armored_infected.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_armored_infected.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_armored_infected.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_armored_infected.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_armored_infected.blocked` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `chaos_armored_infected.suppressed` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_armored_infected.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_armored_infected.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_armored_infected.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_armored_infected.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_armored_infected.running_melee_attack` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_armored_infected.assault_follow` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_armored_infected.alerted` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_armored_infected.idle` |

### chaos_beast_of_nurgle

定义：[chaos_beast_of_nurgle](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_beast_of_nurgle_breed.lua#L1)；行为树：[chaos_beast_of_nurgle](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_beast_of_nurgle_behavior_tree.lua#L1)。

声明的动画变量：`tongue_length`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_beast_of_nurgle.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_beast_of_nurgle.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_beast_of_nurgle.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_beast_of_nurgle.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_beast_of_nurgle.open_door` |
| `death` | [BtBeastOfNurgleDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_die_action.lua#L1) | `chaos_beast_of_nurgle.death` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_beast_of_nurgle.stagger` |
| `weakspot_stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_beast_of_nurgle.weakspot_stagger` |
| `spit_out` | [BtBeastOfNurgleSpitOutAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L1) | `chaos_beast_of_nurgle.spit_out` |
| `fast_movement` | [BtBeastOfNurgleMovementAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L1) | `chaos_beast_of_nurgle.fast_movement` |
| `consume` | [BtBeastOfNurgleConsumeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L1) | `chaos_beast_of_nurgle.consume` |
| `melee_attack_body_slam_aoe` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_body_slam_aoe` |
| `melee_attack_fwd_left` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_fwd_left` |
| `melee_attack_fwd_right` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_fwd_right` |
| `melee_attack_bwd` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_bwd` |
| `melee_attack_left` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_left` |
| `melee_attack_right` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_beast_of_nurgle.melee_attack_right` |
| `align` | [BtBeastOfNurgleAlignAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L1) | `chaos_beast_of_nurgle.align` |
| `alerted` | [BtBeastOfNurgleAlignAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L1) | `chaos_beast_of_nurgle.alerted` |
| `change_target` | [BtChangeTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L1) | `chaos_beast_of_nurgle.change_target` |
| `run_away` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `chaos_beast_of_nurgle.run_away` |
| `consume_minion` | [BtBeastOfNurgleConsumeMinionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L1) | `chaos_beast_of_nurgle.consume_minion` |
| `vomit` | [BtShootLiquidBeamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L1) | `chaos_beast_of_nurgle.vomit` |
| `movement` | [BtBeastOfNurgleMovementAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L1) | `chaos_beast_of_nurgle.movement` |
| `passive_alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_beast_of_nurgle.passive_alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_beast_of_nurgle.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_beast_of_nurgle.idle` |

### chaos_daemonhost

定义：[chaos_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_daemonhost_breed.lua#L1)；行为树：[chaos_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_daemonhost_behavior_tree.lua#L1)。

声明的动画变量：`lean`、`moving_attack_fwd_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death_leave` | [BtChaosDaemonhostDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L1) | `chaos_daemonhost.death_leave` |
| `death` | [BtChaosDaemonhostDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L1) | `chaos_daemonhost.death` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_daemonhost.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_daemonhost.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_daemonhost.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_daemonhost.open_door` |
| `warp_teleport` | [BtWarpTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_warp_teleport_action.lua#L1) | `chaos_daemonhost.warp_teleport` |
| `warp_grab` | [BtChaosDaemonhostWarpGrabAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L1) | `chaos_daemonhost.warp_grab` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_daemonhost.stagger` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_daemonhost.follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_daemonhost.melee_attack` |
| `warp_sweep` | [BtChaosDaemonhostWarpSweepAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L1) | `chaos_daemonhost.warp_sweep` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_daemonhost.combo_attack` |
| `passive` | [BtChaosDaemonhostPassiveAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_passive_action.lua#L1) | `chaos_daemonhost.passive` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_daemonhost.idle` |

### chaos_hound

定义：[chaos_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_hound_breed.lua#L1)；行为树：[chaos_hound](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_hound_behavior_tree.lua#L1)。

声明的动画变量：`gallop_lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_hound.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_hound.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_hound.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_hound.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_hound.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_hound.stagger` |
| `approach_target` | [BtChaosHoundApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L1) | `chaos_hound.approach_target` |
| `leap` | [BtChaosHoundLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L1) | `chaos_hound.leap` |
| `target_pounced` | [BtChaosHoundTargetPouncedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L1) | `chaos_hound.target_pounced` |
| `skulking` | [BtChaosHoundSkulkAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L1) | `chaos_hound.skulking` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_hound.patrol` |
| `roaming` | [BtChaosHoundRoamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L1) | `chaos_hound.roaming` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_hound.idle` |

### chaos_hound_mutator

定义：[chaos_hound_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_hound_mutator_breed.lua#L1)；行为树：[chaos_hound_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_hound_mutator_behavior_tree.lua#L1)。

声明的动画变量：`gallop_lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_hound_mutator.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_hound_mutator.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_hound_mutator.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_hound_mutator.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_hound_mutator.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_hound_mutator.stagger` |
| `approach_target` | [BtChaosHoundApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L1) | `chaos_hound_mutator.approach_target` |
| `leap` | [BtChaosHoundLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L1) | `chaos_hound_mutator.leap` |
| `target_pounced` | [BtChaosHoundTargetPouncedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L1) | `chaos_hound_mutator.target_pounced` |
| `skulking` | [BtChaosHoundSkulkAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L1) | `chaos_hound_mutator.skulking` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_hound_mutator.patrol` |
| `roaming` | [BtChaosHoundRoamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L1) | `chaos_hound_mutator.roaming` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_hound_mutator.idle` |

### chaos_lesser_mutated_poxwalker

定义：[chaos_lesser_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_lesser_mutated_poxwalker_breed.lua#L1)；行为树：[chaos_lesser_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_lesser_mutated_poxwalker_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_lesser_mutated_poxwalker.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_lesser_mutated_poxwalker.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_lesser_mutated_poxwalker.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_lesser_mutated_poxwalker.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_lesser_mutated_poxwalker.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_lesser_mutated_poxwalker.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_lesser_mutated_poxwalker.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_lesser_mutated_poxwalker.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_lesser_mutated_poxwalker.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_lesser_mutated_poxwalker.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_lesser_mutated_poxwalker.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_lesser_mutated_poxwalker.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_lesser_mutated_poxwalker.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_lesser_mutated_poxwalker.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_lesser_mutated_poxwalker.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_lesser_mutated_poxwalker.alerted` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_lesser_mutated_poxwalker.idle` |

### chaos_mutated_poxwalker

定义：[chaos_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutated_poxwalker_breed.lua#L1)；行为树：[chaos_mutated_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutated_poxwalker_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_mutated_poxwalker.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_mutated_poxwalker.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_mutated_poxwalker.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_mutated_poxwalker.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_mutated_poxwalker.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_mutated_poxwalker.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_mutated_poxwalker.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_mutated_poxwalker.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_mutated_poxwalker.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_mutated_poxwalker.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_mutated_poxwalker.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_mutated_poxwalker.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_mutated_poxwalker.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_mutated_poxwalker.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_mutated_poxwalker.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_mutated_poxwalker.alerted` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_mutated_poxwalker.idle` |

### chaos_mutator_daemonhost

定义：[chaos_mutator_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutator_daemonhost_breed.lua#L1)；行为树：[chaos_mutator_daemonhost](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutator_daemonhost_behavior_tree.lua#L1)。

声明的动画变量：`lean`、`moving_attack_fwd_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death_leave` | [BtChaosDaemonhostDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L1) | `chaos_mutator_daemonhost.death_leave` |
| `death` | [BtChaosDaemonhostDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L1) | `chaos_mutator_daemonhost.death` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_mutator_daemonhost.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_mutator_daemonhost.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_mutator_daemonhost.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_mutator_daemonhost.open_door` |
| `warp_teleport` | [BtWarpTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_warp_teleport_action.lua#L1) | `chaos_mutator_daemonhost.warp_teleport` |
| `warp_grab` | [BtChaosDaemonhostWarpGrabAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L1) | `chaos_mutator_daemonhost.warp_grab` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_mutator_daemonhost.stagger` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_mutator_daemonhost.follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_mutator_daemonhost.melee_attack` |
| `warp_sweep` | [BtChaosDaemonhostWarpSweepAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L1) | `chaos_mutator_daemonhost.warp_sweep` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_mutator_daemonhost.combo_attack` |
| `passive` | [BtChaosMutatorDaemonhostPassiveAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_daemonhost_passive_action.lua#L1) | `chaos_mutator_daemonhost.passive` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_mutator_daemonhost.idle` |

### chaos_mutator_ritualist

定义：[chaos_mutator_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_mutator_ritualist_breed.lua#L1)；行为树：[chaos_mutator_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_mutator_ritualist_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_mutator_ritualist.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_mutator_ritualist.disable` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_mutator_ritualist.stagger` |
| `chanting` | [BtChaosMutatorRitualistChantingAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_ritualist_chanting_action.lua#L1) | `chaos_mutator_ritualist.chanting` |

### chaos_newly_infected

定义：[chaos_newly_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_newly_infected_breed.lua#L1)；行为树：[chaos_newly_infected](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_newly_infected_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_newly_infected.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_newly_infected.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_newly_infected.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_newly_infected.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_newly_infected.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_newly_infected.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_newly_infected.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_newly_infected.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_newly_infected.blocked` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `chaos_newly_infected.suppressed` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_newly_infected.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_newly_infected.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_newly_infected.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_newly_infected.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_newly_infected.running_melee_attack` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_newly_infected.assault_follow` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_newly_infected.alerted` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_newly_infected.idle` |

### chaos_ogryn_bulwark

定义：[chaos_ogryn_bulwark](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_bulwark_breed.lua#L1)；行为树：[chaos_ogryn_bulwark](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_bulwark_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_ogryn_bulwark.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_ogryn_bulwark.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_ogryn_bulwark.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_ogryn_bulwark.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_ogryn_bulwark.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_ogryn_bulwark.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_ogryn_bulwark.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_ogryn_bulwark.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `chaos_ogryn_bulwark.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_ogryn_bulwark.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_ogryn_bulwark.blocked` |
| `far_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_ogryn_bulwark.far_follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_ogryn_bulwark.combat_idle` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_ogryn_bulwark.follow` |
| `shield_push` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_bulwark.shield_push` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_bulwark.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_bulwark.moving_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_ogryn_bulwark.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_ogryn_bulwark.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_ogryn_bulwark.idle` |

### chaos_ogryn_executor

定义：[chaos_ogryn_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_executor_breed.lua#L1)；行为树：[chaos_ogryn_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_executor_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_ogryn_executor.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_ogryn_executor.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_ogryn_executor.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_ogryn_executor.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_ogryn_executor.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_ogryn_executor.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_ogryn_executor.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_ogryn_executor.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `chaos_ogryn_executor.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_ogryn_executor.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_ogryn_executor.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_ogryn_executor.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_ogryn_executor.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.melee_attack` |
| `melee_attack_punch` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.melee_attack_punch` |
| `melee_attack_pommel` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.melee_attack_pommel` |
| `melee_attack_kick` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.melee_attack_kick` |
| `melee_attack_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.melee_attack_cleave` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.moving_melee_attack` |
| `moving_melee_attack_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_executor.moving_melee_attack_cleave` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_ogryn_executor.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_ogryn_executor.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_ogryn_executor.idle` |

### chaos_ogryn_gunner

定义：[chaos_ogryn_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_gunner_breed.lua#L1)；行为树：[chaos_ogryn_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_gunner_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_ogryn_gunner.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_ogryn_gunner.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_ogryn_gunner.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_ogryn_gunner.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_ogryn_gunner.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_ogryn_gunner.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_ogryn_gunner.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `chaos_ogryn_gunner.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_ogryn_gunner.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_ogryn_gunner.blocked` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `chaos_ogryn_gunner.suppressed` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `chaos_ogryn_gunner.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `chaos_ogryn_gunner.weapon_malfunction_loop` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_gunner.melee_attack` |
| `melee_attack_push` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_gunner.melee_attack_push` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `chaos_ogryn_gunner.shoot` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `chaos_ogryn_gunner.move_to_combat_vector` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_ogryn_gunner.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_ogryn_gunner.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_ogryn_gunner.idle` |

### chaos_ogryn_houndmaster

定义：[chaos_ogryn_houndmaster](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_ogryn_houndmaster_breed.lua#L1)；行为树：[chaos_ogryn_houndmaster](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_ogryn_houndmaster_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_ogryn_houndmaster.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_ogryn_houndmaster.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_ogryn_houndmaster.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_ogryn_houndmaster.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_ogryn_houndmaster.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_ogryn_houndmaster.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_ogryn_houndmaster.smash_obstacle` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_ogryn_houndmaster.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_ogryn_houndmaster.blocked` |
| `summon` | [BtSummonMinionsAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L1) | `chaos_ogryn_houndmaster.summon` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_ogryn_houndmaster.follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_houndmaster.melee_attack` |
| `charge` | [BtChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L1) | `chaos_ogryn_houndmaster.charge` |
| `far_moving_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_houndmaster.far_moving_attack` |
| `moving_melee_attack_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_ogryn_houndmaster.moving_melee_attack_cleave` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_ogryn_houndmaster.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_ogryn_houndmaster.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_ogryn_houndmaster.idle` |

### chaos_plague_ogryn

定义：[chaos_plague_ogryn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_plague_ogryn_breed.lua#L1)；行为树：[chaos_plague_ogryn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_plague_ogryn_behavior_tree.lua#L1)。

声明的动画变量：`lean`、`moving_attack_fwd_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_plague_ogryn.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_plague_ogryn.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_plague_ogryn.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_plague_ogryn.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_plague_ogryn.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_plague_ogryn.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_plague_ogryn.stagger` |
| `change_target` | [BtChangeTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L1) | `chaos_plague_ogryn.change_target` |
| `melee_slam` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_plague_ogryn.melee_slam` |
| `plague_stomp` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_plague_ogryn.plague_stomp` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_plague_ogryn.combo_attack` |
| `catapult_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_plague_ogryn.catapult_attack` |
| `charge` | [BtChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L1) | `chaos_plague_ogryn.charge` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_plague_ogryn.follow` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_plague_ogryn.idle` |

### chaos_poxwalker_bomber

定义：[chaos_poxwalker_bomber](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_poxwalker_bomber_breed.lua#L1)；行为树：[chaos_poxwalker_bomber](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_poxwalker_bomber_behavior_tree.lua#L1)。

声明的动画变量：本索引未提取到列表。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `explode` | [BtChaosPoxwalkerExplodeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_poxwalker_explode_action.lua#L1) | `chaos_poxwalker_bomber.explode` |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_poxwalker_bomber.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_poxwalker_bomber.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `chaos_poxwalker_bomber.teleport` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_poxwalker_bomber.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_poxwalker_bomber.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_poxwalker_bomber.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_poxwalker_bomber.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_poxwalker_bomber.stagger` |
| `approach` | [BtPoxwalkerBomberApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L1) | `chaos_poxwalker_bomber.approach` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_poxwalker_bomber.idle` |

### chaos_poxwalker

定义：[chaos_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_poxwalker_breed.lua#L1)；行为树：[chaos_poxwalker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_poxwalker_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_poxwalker.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `chaos_poxwalker.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `chaos_poxwalker.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_poxwalker.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_poxwalker.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_poxwalker.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_poxwalker.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_poxwalker.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_poxwalker.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `chaos_poxwalker.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `chaos_poxwalker.follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `chaos_poxwalker.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_poxwalker.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_poxwalker.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_poxwalker.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_poxwalker.alerted` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_poxwalker.idle` |

### chaos_spawn

定义：[chaos_spawn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/chaos/chaos_spawn_breed.lua#L1)；行为树：[chaos_spawn](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/chaos/chaos_spawn_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `chaos_spawn.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `chaos_spawn.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `chaos_spawn.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `chaos_spawn.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `chaos_spawn.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `chaos_spawn.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `chaos_spawn.stagger` |
| `change_target_combo` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_spawn.change_target_combo` |
| `change_target` | [BtChangeTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L1) | `chaos_spawn.change_target` |
| `leap` | [BtLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L1) | `chaos_spawn.leap` |
| `grab` | [BtChaosSpawnGrabAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L1) | `chaos_spawn.grab` |
| `claw_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_spawn.claw_attack` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `chaos_spawn.combo_attack` |
| `erratic_follow` | [BtErraticFollowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L1) | `chaos_spawn.erratic_follow` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `chaos_spawn.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `chaos_spawn.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `chaos_spawn.idle` |

### cultist_assault

定义：[cultist_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_assault_breed.lua#L1)；行为树：[cultist_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_assault_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_assault.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_assault.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_assault.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_assault.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_assault.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_assault.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_assault.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_assault.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_assault.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_assault.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `cultist_assault.switch_weapon` |
| `move_to_cover` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `cultist_assault.move_to_cover` |
| `in_cover` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1) | `cultist_assault.in_cover` |
| `move_to_cover_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_assault.move_to_cover_shoot` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `cultist_assault.suppressed` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `cultist_assault.move_to_combat_vector` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `cultist_assault.melee_combat_idle` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_assault.melee_follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_assault.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_assault.moving_melee_attack` |
| `follow` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `cultist_assault.follow` |
| `assault` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `cultist_assault.assault` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_assault.shoot` |
| `run_stop_and_shoot` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1) | `cultist_assault.run_stop_and_shoot` |
| `shoot_close` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_assault.shoot_close` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_assault.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_assault.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_assault.idle` |

### cultist_berzerker

定义：[cultist_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_berzerker_breed.lua#L1)；行为树：[cultist_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_berzerker_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_berzerker.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_berzerker.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_berzerker.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_berzerker.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_berzerker.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_berzerker.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_berzerker.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `cultist_berzerker.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_berzerker.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_berzerker.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_berzerker.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_berzerker.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_berzerker.assault_follow` |
| `leap_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_berzerker.leap_attack` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_berzerker.combo_attack` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_berzerker.melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_berzerker.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_berzerker.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_berzerker.idle` |

### cultist_captain

定义：[cultist_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_captain_breed.lua#L1)；行为树：[cultist_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_captain_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_captain.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_captain.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_captain.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_captain.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `cultist_captain.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_captain.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_captain.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_captain.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `cultist_captain.switch_weapon` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_captain.use_stim` |
| `kick` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.kick` |
| `punch` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.punch` |
| `throw_fire_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `cultist_captain.throw_fire_grenade` |
| `charge` | [BtChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L1) | `cultist_captain.charge` |
| `void_shield_explosion` | [BtVoidShieldExplosionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L1) | `cultist_captain.void_shield_explosion` |
| `melee_follow_powermaul` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_captain.melee_follow_powermaul` |
| `powermaul_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.powermaul_melee_attack` |
| `powermaul_melee_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.powermaul_melee_cleave` |
| `powermaul_moving_melee_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.powermaul_moving_melee_cleave` |
| `powermaul_ground_slam` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.powermaul_ground_slam` |
| `powermaul_pommel` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.powermaul_pommel` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `cultist_captain.melee_combat_idle` |
| `melee_follow_power_sword` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_captain.melee_follow_power_sword` |
| `power_sword_melee_combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.power_sword_melee_combo_attack` |
| `power_sword_melee_sweep` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.power_sword_melee_sweep` |
| `power_sword_moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.power_sword_moving_melee_attack` |
| `power_sword_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_captain.power_sword_melee_attack` |
| `ranged_follow` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `cultist_captain.ranged_follow` |
| `hellgun_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.hellgun_shoot` |
| `hellgun_spray_and_pray` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.hellgun_spray_and_pray` |
| `bolt_pistol_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.bolt_pistol_shoot` |
| `plasma_pistol_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.plasma_pistol_shoot` |
| `plasma_pistol_shoot_volley` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.plasma_pistol_shoot_volley` |
| `approach_target` | [BtRenegadeNetgunnerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L1) | `cultist_captain.approach_target` |
| `shoot_net` | [BtShootNetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L1) | `cultist_captain.shoot_net` |
| `shotgun_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_captain.shotgun_shoot` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_captain.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_captain.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_captain.idle` |

### cultist_flamer

定义：[cultist_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_flamer_breed.lua#L1)；行为树：[cultist_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_flamer_behavior_tree.lua#L1)。

声明的动画变量：`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `explode` | [BtFlamerCheckBackpackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_check_backpack_action.lua#L1) | `cultist_flamer.explode` |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_flamer.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_flamer.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_flamer.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_flamer.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_flamer.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_flamer.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_flamer.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_flamer.stagger` |
| `weapon_malfunction_run_to_spawner` | [BtMoveToPositionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L1) | `cultist_flamer.weapon_malfunction_run_to_spawner` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `cultist_flamer.weapon_malfunction_loop` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_flamer.melee_attack` |
| `follow` | [BtFlamerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L1) | `cultist_flamer.follow` |
| `shoot` | [BtShootLiquidBeamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L1) | `cultist_flamer.shoot` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_flamer.idle` |

### cultist_grenadier

定义：[cultist_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_grenadier_breed.lua#L1)；行为树：[cultist_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_grenadier_behavior_tree.lua#L1)。

声明的动画变量：本索引未提取到列表。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_grenadier.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_grenadier.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_grenadier.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_grenadier.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_grenadier.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_grenadier.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_grenadier.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_grenadier.stagger` |
| `quick_throw_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `cultist_grenadier.quick_throw_grenade` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `cultist_grenadier.move_to_combat_vector` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_grenadier.melee_attack` |
| `follow` | [BtGrenadierFollowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L1) | `cultist_grenadier.follow` |
| `throw_grenade` | [BtGrenadierThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L1) | `cultist_grenadier.throw_grenade` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_grenadier.idle` |

### cultist_gunner

定义：[cultist_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_gunner_breed.lua#L1)；行为树：[cultist_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_gunner_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_gunner.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_gunner.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_gunner.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_gunner.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_gunner.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_gunner.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_gunner.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_gunner.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_gunner.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_gunner.blocked` |
| `move_to_cover_weapon_malfunction` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `cultist_gunner.move_to_cover_weapon_malfunction` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `cultist_gunner.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `cultist_gunner.weapon_malfunction_loop` |
| `move_to_cover` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `cultist_gunner.move_to_cover` |
| `in_cover` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1) | `cultist_gunner.in_cover` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `cultist_gunner.suppressed` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `cultist_gunner.move_to_combat_vector` |
| `bayonet_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_gunner.bayonet_melee_attack` |
| `shoot_spray_n_pray` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_gunner.shoot_spray_n_pray` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_gunner.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_gunner.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_gunner.idle` |

### cultist_melee

定义：[cultist_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_melee_breed.lua#L1)；行为树：[cultist_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_melee_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_melee.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_melee.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_melee.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_melee.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_melee.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_melee.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_melee.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `cultist_melee.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_melee.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_melee.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_melee.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_melee.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_melee.assault_follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `cultist_melee.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_melee.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_melee.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_melee.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_melee.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_melee.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_melee.idle` |

### cultist_mutant

定义：[cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_mutant_breed.lua#L1)；行为树：[cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_mutant_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_mutant.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_mutant.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_mutant.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_mutant.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_mutant.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_mutant.stagger` |
| `charge` | [BtMutantChargerChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1) | `cultist_mutant.charge` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_mutant.idle` |

### cultist_mutant_mutator

定义：[cultist_mutant_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_mutant_mutator_breed.lua#L1)；行为树：[cultist_mutant](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_mutant_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_mutant.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_mutant.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_mutant.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_mutant.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_mutant.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_mutant.stagger` |
| `charge` | [BtMutantChargerChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1) | `cultist_mutant.charge` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_mutant.idle` |

### cultist_ritualist

定义：[cultist_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_ritualist_breed.lua#L1)；行为树：[cultist_ritualist](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_ritualist_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_ritualist.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_ritualist.disable` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_ritualist.stagger` |
| `chanting` | [BtCultistRitualistChantingAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_cultist_ritualist_chanting_action.lua#L1) | `cultist_ritualist.chanting` |

### cultist_shocktrooper

定义：[cultist_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_shocktrooper_breed.lua#L1)；行为树：[cultist_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_shocktrooper_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_shocktrooper.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `cultist_shocktrooper.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_shocktrooper.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_shocktrooper.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_shocktrooper.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_shocktrooper.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_shocktrooper.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_shocktrooper.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_shocktrooper.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_shocktrooper.blocked` |
| `bayonet_charge_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_shocktrooper.bayonet_charge_attack` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_shocktrooper.melee_follow` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `cultist_shocktrooper.melee_combat_idle` |
| `bayonet_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_shocktrooper.bayonet_melee_attack` |
| `assault` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `cultist_shocktrooper.assault` |
| `run_stop_and_shoot` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1) | `cultist_shocktrooper.run_stop_and_shoot` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `cultist_shocktrooper.move_to_combat_vector` |
| `step_shoot` | [BtStepShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L1) | `cultist_shocktrooper.step_shoot` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `cultist_shocktrooper.shoot` |
| `ranged_follow_no_los` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `cultist_shocktrooper.ranged_follow_no_los` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_shocktrooper.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_shocktrooper.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_shocktrooper.idle` |

### cultist_vanguard

定义：[cultist_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/cultist/cultist_vanguard_breed.lua#L1)；行为树：[cultist_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/cultist/cultist_vanguard_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `cultist_vanguard.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `cultist_vanguard.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `cultist_vanguard.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `cultist_vanguard.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `cultist_vanguard.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `cultist_vanguard.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `cultist_vanguard.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `cultist_vanguard.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `cultist_vanguard.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `cultist_vanguard.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_vanguard.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `cultist_vanguard.assault_follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `cultist_vanguard.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_vanguard.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_vanguard.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `cultist_vanguard.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `cultist_vanguard.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `cultist_vanguard.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `cultist_vanguard.idle` |

### renegade_assault

定义：[renegade_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_assault_breed.lua#L1)；行为树：[renegade_assault](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_assault_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_assault.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_assault.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_assault.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_assault.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_assault.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_assault.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_assault.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_assault.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_assault.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_assault.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `renegade_assault.switch_weapon` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `renegade_assault.suppressed` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_assault.move_to_combat_vector` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_assault.melee_combat_idle` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_assault.melee_follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_assault.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_assault.moving_melee_attack` |
| `follow` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_assault.follow` |
| `assault` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_assault.assault` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_assault.shoot` |
| `run_stop_and_shoot` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1) | `renegade_assault.run_stop_and_shoot` |
| `ranged_follow_no_los` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_assault.ranged_follow_no_los` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_assault.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_assault.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_assault.idle` |

### renegade_berzerker

定义：[renegade_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_berzerker_breed.lua#L1)；行为树：[renegade_berzerker](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_berzerker_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_berzerker.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_berzerker.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_berzerker.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_berzerker.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_berzerker.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_berzerker.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_berzerker.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_berzerker.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_berzerker.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_berzerker.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_berzerker.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_berzerker.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_berzerker.assault_follow` |
| `combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_berzerker.combo_attack` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_berzerker.melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_berzerker.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_berzerker.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_berzerker.idle` |

### renegade_captain

定义：[renegade_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_captain_breed.lua#L1)；行为树：[renegade_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_captain_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_captain.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_captain.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_captain.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_captain.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_captain.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_captain.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_captain.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_captain.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `renegade_captain.switch_weapon` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_captain.use_stim` |
| `kick` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.kick` |
| `punch` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.punch` |
| `throw_fire_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `renegade_captain.throw_fire_grenade` |
| `charge` | [BtChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L1) | `renegade_captain.charge` |
| `void_shield_explosion` | [BtVoidShieldExplosionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L1) | `renegade_captain.void_shield_explosion` |
| `melee_follow_powermaul` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_captain.melee_follow_powermaul` |
| `powermaul_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.powermaul_melee_attack` |
| `powermaul_melee_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.powermaul_melee_cleave` |
| `powermaul_moving_melee_cleave` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.powermaul_moving_melee_cleave` |
| `powermaul_ground_slam` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.powermaul_ground_slam` |
| `powermaul_pommel` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.powermaul_pommel` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_captain.melee_combat_idle` |
| `melee_follow_power_sword` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_captain.melee_follow_power_sword` |
| `power_sword_melee_combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.power_sword_melee_combo_attack` |
| `power_sword_melee_sweep` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.power_sword_melee_sweep` |
| `power_sword_moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.power_sword_moving_melee_attack` |
| `power_sword_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_captain.power_sword_melee_attack` |
| `ranged_follow` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_captain.ranged_follow` |
| `hellgun_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.hellgun_shoot` |
| `hellgun_spray_and_pray` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.hellgun_spray_and_pray` |
| `bolt_pistol_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.bolt_pistol_shoot` |
| `plasma_pistol_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.plasma_pistol_shoot` |
| `plasma_pistol_shoot_volley` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.plasma_pistol_shoot_volley` |
| `approach_target` | [BtRenegadeNetgunnerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L1) | `renegade_captain.approach_target` |
| `shoot_net` | [BtShootNetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L1) | `renegade_captain.shoot_net` |
| `shotgun_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_captain.shotgun_shoot` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_captain.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_captain.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_captain.idle` |

### renegade_executor

定义：[renegade_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_executor_breed.lua#L1)；行为树：[renegade_executor](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_executor_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_executor.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_executor.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_executor.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_executor.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_executor.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_executor.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_executor.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_executor.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_executor.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_executor.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_executor.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_executor.follow` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_executor.melee_attack` |
| `melee_cleave_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_executor.melee_cleave_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_executor.moving_melee_attack` |
| `moving_melee_cleave_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_executor.moving_melee_cleave_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_executor.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_executor.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_executor.idle` |

### renegade_flamer

定义：[renegade_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_flamer_breed.lua#L1)；行为树：[renegade_flamer](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_flamer_behavior_tree.lua#L1)。

声明的动画变量：`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `explode` | [BtFlamerCheckBackpackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_check_backpack_action.lua#L1) | `renegade_flamer.explode` |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_flamer.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_flamer.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_flamer.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_flamer.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_flamer.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_flamer.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_flamer.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_flamer.stagger` |
| `weapon_malfunction_run_to_spawner` | [BtMoveToPositionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L1) | `renegade_flamer.weapon_malfunction_run_to_spawner` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_flamer.weapon_malfunction_loop` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_flamer.melee_attack` |
| `follow` | [BtFlamerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L1) | `renegade_flamer.follow` |
| `shoot` | [BtShootLiquidBeamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L1) | `renegade_flamer.shoot` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_flamer.idle` |

### renegade_flamer_mutator

定义：[renegade_flamer_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_flamer_mutator_breed.lua#L1)；行为树：[renegade_flamer_mutator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_flamer_mutator_behavior_tree.lua#L1)。

声明的动画变量：`lean`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_flamer_mutator.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_flamer_mutator.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_flamer_mutator.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_flamer_mutator.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_flamer_mutator.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_flamer_mutator.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_flamer_mutator.stagger` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_flamer_mutator.weapon_malfunction_loop` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_flamer_mutator.melee_attack` |
| `follow` | [BtFlamerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L1) | `renegade_flamer_mutator.follow` |
| `shoot` | [BtShootLiquidBeamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L1) | `renegade_flamer_mutator.shoot` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_flamer_mutator.alerted` |
| `aggroed_patrol` | [BtRenegadeFlamerPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L1) | `renegade_flamer_mutator.aggroed_patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_flamer_mutator.idle` |

### renegade_grenadier

定义：[renegade_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_grenadier_breed.lua#L1)；行为树：[renegade_grenadier](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_grenadier_behavior_tree.lua#L1)。

声明的动画变量：本索引未提取到列表。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_grenadier.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_grenadier.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_grenadier.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_grenadier.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_grenadier.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_grenadier.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_grenadier.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_grenadier.stagger` |
| `quick_throw_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `renegade_grenadier.quick_throw_grenade` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_grenadier.move_to_combat_vector` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_grenadier.melee_attack` |
| `follow` | [BtGrenadierFollowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L1) | `renegade_grenadier.follow` |
| `throw_grenade` | [BtGrenadierThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L1) | `renegade_grenadier.throw_grenade` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_grenadier.idle` |

### renegade_gunner

定义：[renegade_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_gunner_breed.lua#L1)；行为树：[renegade_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_gunner_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_gunner.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_gunner.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_gunner.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_gunner.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_gunner.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_gunner.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_gunner.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_gunner.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_gunner.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_gunner.blocked` |
| `move_to_cover_weapon_malfunction` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_gunner.move_to_cover_weapon_malfunction` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_gunner.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_gunner.weapon_malfunction_loop` |
| `move_to_cover` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_gunner.move_to_cover` |
| `in_cover` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1) | `renegade_gunner.in_cover` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `renegade_gunner.suppressed` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_gunner.move_to_combat_vector` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_gunner.melee_attack` |
| `shoot_spray_n_pray` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_gunner.shoot_spray_n_pray` |
| `escape_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_gunner.escape_to_combat_vector` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_gunner.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_gunner.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_gunner.idle` |

### renegade_melee

定义：[renegade_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_melee_breed.lua#L1)；行为树：[renegade_melee](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_melee_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_melee.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_melee.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_melee.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_melee.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_melee.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_melee.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_melee.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_melee.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_melee.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_melee.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_melee.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_melee.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_melee.assault_follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_melee.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_melee.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_melee.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_melee.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_melee.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_melee.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_melee.idle` |

### renegade_netgunner

定义：[renegade_netgunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_netgunner_breed.lua#L1)；行为树：[renegade_netgunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_netgunner_behavior_tree.lua#L1)。

声明的动画变量：本索引未提取到列表。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_netgunner.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_netgunner.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_netgunner.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_netgunner.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_netgunner.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_netgunner.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_netgunner.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_netgunner.stagger` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_netgunner.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_netgunner.weapon_malfunction_loop` |
| `approach_target` | [BtRenegadeNetgunnerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L1) | `renegade_netgunner.approach_target` |
| `shoot_net` | [BtShootNetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L1) | `renegade_netgunner.shoot_net` |
| `reload` | [BtReloadAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_reload_action.lua#L1) | `renegade_netgunner.reload` |
| `run_away` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_netgunner.run_away` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_netgunner.idle` |

### renegade_plasma_gunner

定义：[renegade_plasma_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_plasma_gunner_breed.lua#L1)；行为树：[renegade_plasma_gunner](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_plasma_gunner_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`、`moving_attack_fwd_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_plasma_gunner.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_plasma_gunner.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_plasma_gunner.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_plasma_gunner.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_plasma_gunner.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_plasma_gunner.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_plasma_gunner.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_plasma_gunner.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_plasma_gunner.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_plasma_gunner.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `renegade_plasma_gunner.switch_weapon` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_plasma_gunner.melee_follow` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_plasma_gunner.melee_combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_plasma_gunner.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_plasma_gunner.moving_melee_attack` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_plasma_gunner.move_to_combat_vector` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_plasma_gunner.shoot` |
| `ranged_follow_no_los` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_plasma_gunner.ranged_follow_no_los` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_plasma_gunner.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_plasma_gunner.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_plasma_gunner.idle` |

### renegade_radio_operator

定义：[renegade_radio_operator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_radio_operator_breed.lua#L1)；行为树：[renegade_radio_operator](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_radio_operator_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_radio_operator.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_radio_operator.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_radio_operator.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_radio_operator.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_radio_operator.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_radio_operator.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_radio_operator.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_radio_operator.blocked` |
| `move_to_cover_weapon_malfunction` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_radio_operator.move_to_cover_weapon_malfunction` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_radio_operator.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_radio_operator.weapon_malfunction_loop` |
| `summon` | [BtSummonMinionsAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L1) | `renegade_radio_operator.summon` |
| `move_to_cover` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_radio_operator.move_to_cover` |
| `in_cover` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1) | `renegade_radio_operator.in_cover` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `renegade_radio_operator.suppressed` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_radio_operator.move_to_combat_vector` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_radio_operator.melee_attack` |
| `shoot_spray_n_pray` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_radio_operator.shoot_spray_n_pray` |
| `escape_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_radio_operator.escape_to_combat_vector` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_radio_operator.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_radio_operator.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_radio_operator.idle` |

### renegade_rifleman

定义：[renegade_rifleman](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_rifleman_breed.lua#L1)；行为树：[renegade_rifleman](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_rifleman_behavior_tree.lua#L1)。

声明的动画变量：`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_rifleman.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_rifleman.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_rifleman.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_rifleman.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_rifleman.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_rifleman.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_rifleman.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_rifleman.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_rifleman.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_rifleman.blocked` |
| `move_to_cover_weapon_malfunction` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_rifleman.move_to_cover_weapon_malfunction` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_rifleman.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_rifleman.weapon_malfunction_loop` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `renegade_rifleman.switch_weapon` |
| `move_to_cover` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_rifleman.move_to_cover` |
| `in_cover` | [BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1) | `renegade_rifleman.in_cover` |
| `move_to_cover_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_rifleman.move_to_cover_shoot` |
| `suppressed` | [BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1) | `renegade_rifleman.suppressed` |
| `bayonet_charge_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_rifleman.bayonet_charge_attack` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_rifleman.melee_follow` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_rifleman.melee_combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_rifleman.melee_attack` |
| `move_to_combat_vector_far` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_rifleman.move_to_combat_vector_far` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_rifleman.shoot` |
| `far_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_rifleman.far_combat_idle` |
| `close_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_rifleman.close_combat_idle` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_rifleman.move_to_combat_vector` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_rifleman.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_rifleman.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_rifleman.idle` |

### renegade_shocktrooper

定义：[renegade_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_shocktrooper_breed.lua#L1)；行为树：[renegade_shocktrooper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_shocktrooper_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`、`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_shocktrooper.death` |
| `vortex_grabbed` | [BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1) | `renegade_shocktrooper.vortex_grabbed` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_shocktrooper.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_shocktrooper.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_shocktrooper.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_shocktrooper.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_shocktrooper.open_door` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_shocktrooper.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_shocktrooper.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_shocktrooper.blocked` |
| `switch_weapon` | [BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1) | `renegade_shocktrooper.switch_weapon` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_shocktrooper.melee_follow` |
| `melee_combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_shocktrooper.melee_combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_shocktrooper.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_shocktrooper.moving_melee_attack` |
| `assault` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_shocktrooper.assault` |
| `run_stop_and_shoot` | [BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1) | `renegade_shocktrooper.run_stop_and_shoot` |
| `move_to_combat_vector` | [BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1) | `renegade_shocktrooper.move_to_combat_vector` |
| `step_shoot` | [BtStepShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L1) | `renegade_shocktrooper.step_shoot` |
| `shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_shocktrooper.shoot` |
| `ranged_follow_no_los` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_shocktrooper.ranged_follow_no_los` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_shocktrooper.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_shocktrooper.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_shocktrooper.idle` |

### renegade_sniper

定义：[renegade_sniper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_sniper_breed.lua#L1)；行为树：[renegade_sniper](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_sniper_behavior_tree.lua#L1)。

声明的动画变量：`lean`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_sniper.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_sniper.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_sniper.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_sniper.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_sniper.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_sniper.open_door` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_sniper.stagger` |
| `move_to_cover_weapon_malfunction` | [BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1) | `renegade_sniper.move_to_cover_weapon_malfunction` |
| `run_away_weapon_malfunction` | [BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1) | `renegade_sniper.run_away_weapon_malfunction` |
| `weapon_malfunction_loop` | [BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1) | `renegade_sniper.weapon_malfunction_loop` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_sniper.melee_attack` |
| `movement` | [BtSniperMovementAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_movement_action.lua#L1) | `renegade_sniper.movement` |
| `shoot` | [BtSniperShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L1) | `renegade_sniper.shoot` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_sniper.idle` |

### renegade_twin_captain

定义：[renegade_twin_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_twin_captain_breed.lua#L1)；行为树：[renegade_twin_captain](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_twin_captain_behavior_tree.lua#L1)。

声明的动画变量：本索引未提取到列表。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_twin_captain.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_twin_captain.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_twin_captain.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_twin_captain.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_twin_captain.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_twin_captain.open_door` |
| `disappear_instant` | [BtRenegadeTwinCaptainDisappearAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L1) | `renegade_twin_captain.disappear_instant` |
| `disappear` | [BtRenegadeTwinCaptainDisappearAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L1) | `renegade_twin_captain.disappear` |
| `disappear_idle` | [BtTwinCaptainDisappearIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_disappear_idle_action.lua#L1) | `renegade_twin_captain.disappear_idle` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_twin_captain.stagger` |
| `shield_down_recharge` | [BtRenegadeTwinCaptainShieldDownAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L1) | `renegade_twin_captain.shield_down_recharge` |
| `intro` | [BtTwinCaptainIntroAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L1) | `renegade_twin_captain.intro` |
| `kick` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_twin_captain.kick` |
| `ranged_follow` | [BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1) | `renegade_twin_captain.ranged_follow` |
| `plasma_pistol_shoot` | [BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1) | `renegade_twin_captain.plasma_pistol_shoot` |
| `void_shield_explosion` | [BtVoidShieldExplosionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L1) | `renegade_twin_captain.void_shield_explosion` |
| `multiple_quick_throw_grenade_empowered` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `renegade_twin_captain.multiple_quick_throw_grenade_empowered` |
| `quick_throw_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `renegade_twin_captain.quick_throw_grenade` |
| `multiple_quick_throw_grenade` | [BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1) | `renegade_twin_captain.multiple_quick_throw_grenade` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_twin_captain.idle` |

### renegade_twin_captain_two

定义：[renegade_twin_captain_two](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_twin_captain_two_breed.lua#L1)；行为树：[renegade_twin_captain_two](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_twin_captain_two_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_twin_captain_two.death` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_twin_captain_two.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_twin_captain_two.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_twin_captain_two.jump_across` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_twin_captain_two.smash_obstacle` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_twin_captain_two.open_door` |
| `disappear_instant` | [BtRenegadeTwinCaptainDisappearAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L1) | `renegade_twin_captain_two.disappear_instant` |
| `disappear` | [BtRenegadeTwinCaptainDisappearAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L1) | `renegade_twin_captain_two.disappear` |
| `disappear_idle` | [BtTwinCaptainDisappearIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_disappear_idle_action.lua#L1) | `renegade_twin_captain_two.disappear_idle` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_twin_captain_two.stagger` |
| `shield_down_recharge` | [BtRenegadeTwinCaptainShieldDownAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L1) | `renegade_twin_captain_two.shield_down_recharge` |
| `intro` | [BtTwinCaptainIntroAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L1) | `renegade_twin_captain_two.intro` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_twin_captain_two.blocked` |
| `melee_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_twin_captain_two.melee_follow` |
| `kick` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_twin_captain_two.kick` |
| `dash` | [BtDashAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L1) | `renegade_twin_captain_two.dash` |
| `random_dash` | [BtDashAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L1) | `renegade_twin_captain_two.random_dash` |
| `power_sword_melee_sweep` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_twin_captain_two.power_sword_melee_sweep` |
| `dash_fast` | [BtDashAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L1) | `renegade_twin_captain_two.dash_fast` |
| `random_dash_short` | [BtDashAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L1) | `renegade_twin_captain_two.random_dash_short` |
| `power_sword_melee_combo_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_twin_captain_two.power_sword_melee_combo_attack` |
| `power_sword_moving_melee_sweep` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_twin_captain_two.power_sword_moving_melee_sweep` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_twin_captain_two.idle` |

### renegade_vanguard

定义：[renegade_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/settings/breed/breeds/renegade/renegade_vanguard_breed.lua#L1)；行为树：[renegade_vanguard](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_vanguard_behavior_tree.lua#L1)。

声明的动画变量：`moving_attack_fwd_speed`、`anim_move_speed`。

| 节点名 | 动作实现 | 动作数据引用 |
| --- | --- | --- |
| `death` | [BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1) | `renegade_vanguard.death` |
| `disable` | [BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1) | `renegade_vanguard.disable` |
| `exit_spawner` | [BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1) | `renegade_vanguard.exit_spawner` |
| `teleport` | [BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1) | `—` |
| `climb` | [BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1) | `renegade_vanguard.climb` |
| `jump_across` | [BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1) | `renegade_vanguard.jump_across` |
| `open_door` | [BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1) | `renegade_vanguard.open_door` |
| `smash_obstacle` | [BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1) | `renegade_vanguard.smash_obstacle` |
| `use_stim` | [BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1) | `renegade_vanguard.use_stim` |
| `stagger` | [BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1) | `renegade_vanguard.stagger` |
| `blocked` | [BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1) | `renegade_vanguard.blocked` |
| `follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_vanguard.follow` |
| `assault_follow` | [BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1) | `renegade_vanguard.assault_follow` |
| `combat_idle` | [BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1) | `renegade_vanguard.combat_idle` |
| `melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_vanguard.melee_attack` |
| `moving_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_vanguard.moving_melee_attack` |
| `running_melee_attack` | [BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1) | `renegade_vanguard.running_melee_attack` |
| `alerted` | [BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1) | `renegade_vanguard.alerted` |
| `patrol` | [BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1) | `renegade_vanguard.patrol` |
| `idle` | [BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1) | `renegade_vanguard.idle` |

## 动作实现中的计时与速度入口

下面自动索引实际被这些树引用的 77 个动作实现。字段来自直接 `action_data.<字段>` 访问，按 time/timing/duration/cooldown/delay/interval/speed/velocity/acceleration/frequency 筛选；它是定位工具，不保证穷尽间接索引、难度表、黑板组件或辅助函数中的全部参数。字段出现不等于该字段是攻速，也不代表原版已有倍率支持。

“直接属性词”仅表示实现文件中出现该属性；共享射击的间接消费另列。函数和字段均链接到原始行。

### BtAlertedAction

[BtAlertedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `alerted_duration` | [47](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L47) |
| `alerted_durations` | [68](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L68) |
| `start_move_rotation_timings` | [277](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_alerted_action.lua#L277) |

### BtBeastOfNurgleAlignAction

[BtBeastOfNurgleAlignAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_speed` | [31](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L31) |
| `start_move_rotation_timings` | [107](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L107) |
| `align_durations` | [113](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L113) |
| `align_rotation_durations` | [117](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L117) |
| `start_rotation_durations` | [138](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_align_action.lua#L138) |

### BtBeastOfNurgleConsumeAction

[BtBeastOfNurgleConsumeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `consume_durations` | [164](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L164) |
| `damage_timings` | [168](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L168) |
| `consume_timing` | [173](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L173) |
| `throw_timing` | [278](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L278) |
| `throw_duration` | [279](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L279) |
| `rotation_speed` | [282](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L282) |
| `after_throw_taunt_duration` | [364](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_action.lua#L364) |

### BtBeastOfNurgleConsumeMinionAction

[BtBeastOfNurgleConsumeMinionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `cooldown` | [45](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L45) |
| `tongue_out_durations` | [147](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L147) |
| `tongue_in_durations` | [188](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L188) |
| `consume_durations` | [192](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L192) |
| `heal_durations` | [196](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_consume_minion_action.lua#L196) |

### BtBeastOfNurgleDieAction

[BtBeastOfNurgleDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_die_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `explosion_timing` | [17](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_die_action.lua#L17) |
| `death_timings` | [42](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_die_action.lua#L42) |

### BtBeastOfNurgleMovementAction

[BtBeastOfNurgleMovementAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `move_speed` | [60](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L60) |
| `rotation_speed` | [62](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L62) |
| `push_nearby_players_frequency` | [80](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L80) |
| `start_move_rotation_timings` | [199](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L199) |
| `start_rotation_durations` | [226](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L226) |
| `move_to_fail_cooldown` | [300](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L300) |
| `move_to_cooldown` | [314](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_movement_action.lua#L314) |

### BtBeastOfNurgleSpitOutAction

[BtBeastOfNurgleSpitOutAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `align_duration` | [147](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L147) |
| `rotation_speed` | [150](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L150) |
| `throw_timing` | [206](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L206) |
| `throw_duration` | [207](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L207) |
| `after_throw_taunt_duration` | [257](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_beast_of_nurgle_spit_out_action.lua#L257) |

### BtBlockedAction

[BtBlockedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L1)。

直接属性词：[`melee_attack_speed`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L25)。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `blocked_duration` | [54](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_blocked_action.lua#L54) |

### BtChangeTargetAction

[BtChangeTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `move_speed` | [14](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L14) |
| `rotation_speed` | [25](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L25) |
| `change_target_rotation_timings` | [112](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L112) |
| `change_target_rotation_durations` | [120](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L120) |
| `change_target_event_anim_speed_durations` | [123](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_change_target_action.lua#L123) |

### BtChaosDaemonhostDieAction

[BtChaosDaemonhostDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `durations` | [31](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_die_action.lua#L31) |

### BtChaosDaemonhostPassiveAction

[BtChaosDaemonhostPassiveAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_passive_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtChaosDaemonhostWarpGrabAction

[BtChaosDaemonhostWarpGrabAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `fire_timing` | [86](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L86) |
| `execute_timing` | [159](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L159) |
| `execute_duration` | [163](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_grab_action.lua#L163) |

### BtChaosDaemonhostWarpSweepAction

[BtChaosDaemonhostWarpSweepAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `cooldown_duration` | [53](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L53) |
| `attack_anim_durations` | [83](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L83) |
| `attack_anim_damage_timings` | [88](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L88) |
| `attack_move_speed` | [93](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_daemonhost_warp_sweep_action.lua#L93) |

### BtChaosHoundApproachAction

[BtChaosHoundApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [29](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L29) |
| `rotation_speed` | [39](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L39) |
| `trigger_player_alert_vo_frequency` | [105](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L105) |
| `start_move_rotation_timings` | [303](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L303) |
| `start_move_event_anim_speed_durations` | [312](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_approach_action.lua#L312) |

### BtChaosHoundLeapAction

[BtChaosHoundLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `aoe_bot_threat_timing` | [71](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L71) |
| `start_duration_short` | [80](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L80) |
| `start_duration` | [83](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L83) |
| `start_move_speed` | [237](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L237) |
| `stop_duration` | [414](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L414) |
| `aoe_bot_threat_duration` | [419](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L419) |
| `in_air_stagger_duration` | [637](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L637) |
| `wall_jump_speed` | [735](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L735) |
| `wall_jump_align_rotation_speed` | [746](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L746) |
| `wall_jump_rotation_timing` | [748](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L748) |
| `wall_jump_rotation_duration` | [749](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L749) |
| `landing_duration` | [781](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L781) |
| `land_impact_timing` | [794](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L794) |
| `wall_land_duration` | [834](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action.lua#L834) |

### BtChaosHoundRoamAction

[BtChaosHoundRoamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [31](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L31) |
| `rotation_speed` | [37](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L37) |
| `start_move_rotation_timings` | [149](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L149) |
| `start_move_event_anim_speed_durations` | [158](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_roam_action.lua#L158) |

### BtChaosHoundSkulkAction

[BtChaosHoundSkulkAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [28](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L28) |
| `rotation_speed` | [34](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L34) |
| `start_move_rotation_timings` | [127](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L127) |
| `start_move_event_anim_speed_durations` | [136](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_skulk_action.lua#L136) |

### BtChaosHoundTargetPouncedAction

[BtChaosHoundTargetPouncedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `lerp_position_time` | [30](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L30) |
| `damage_frequency` | [180](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L180) |
| `damage_start_time` | [208](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_target_pounced_action.lua#L208) |

### BtChaosMutatorDaemonhostPassiveAction

[BtChaosMutatorDaemonhostPassiveAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_daemonhost_passive_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `ritual_timings` | [52](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_daemonhost_passive_action.lua#L52) |
| `half_time_multiplier` | [316](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_daemonhost_passive_action.lua#L316) |

### BtChaosMutatorRitualistChantingAction

[BtChaosMutatorRitualistChantingAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_mutator_ritualist_chanting_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtChaosPoxwalkerExplodeAction

[BtChaosPoxwalkerExplodeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_poxwalker_explode_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtChaosSpawnGrabAction

[BtChaosSpawnGrabAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `cooldown` | [79](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L79) |
| `total_grab_durations` | [199](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L199) |
| `grab_durations` | [203](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L203) |
| `grab_durations_missed` | [207](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L207) |
| `damage_timings` | [211](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L211) |
| `grab_timings` | [216](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L216) |
| `rotation_durations` | [219](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L219) |
| `start_eat_timings` | [246](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L246) |
| `smash_sweep_start_timings` | [384](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L384) |
| `smash_timings` | [391](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L391) |
| `smash_durations` | [397](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L397) |
| `sweep_ground_impact_fx_timing` | [401](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L401) |
| `throw_timing` | [542](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L542) |
| `throw_duration` | [550](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L550) |
| `rotation_speed` | [560](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L560) |
| `after_throw_taunt_duration` | [683](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_chaos_spawn_grab_action.lua#L683) |

### BtChargeAction

[BtChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `max_duration` | [54](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L54) |
| `charge_speed_min` | [159](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L159) |
| `min_time_navigating` | [187](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L187) |
| `rotation_speed` | [189](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L189) |
| `charge_speed_max` | [211](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L211) |
| `charge_max_speed_at` | [212](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L212) |
| `close_attack_speed` | [217](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L217) |
| `dodge_rotation_speed` | [257](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L257) |
| `close_rotation_speed` | [257](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L257) |
| `min_time_spent_charging` | [262](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L262) |
| `miss_durations` | [271](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L271) |
| `can_hit_wall_durations` | [275](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L275) |
| `wall_stun_time` | [378](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L378) |
| `attack_anim_duration` | [538](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L538) |
| `attack_anim_damage_timing` | [548](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L548) |
| `close_attack_anim_duration` | [568](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L568) |
| `close_attack_anim_damage_timing` | [587](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L587) |
| `start_move_rotation_timings` | [669](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L669) |
| `charge_direction_durations` | [681](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L681) |
| `charge_durations` | [698](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_charge_action.lua#L698) |

### BtClimbAction

[BtClimbAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_duration` | [113](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L113) |
| `anim_timings` | [129](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L129) |
| `blend_timings` | [135](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L135) |
| `land_timings` | [348](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_climb_action.lua#L348) |

### BtCombatIdleAction

[BtCombatIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_combat_idle_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtCultistRitualistChantingAction

[BtCultistRitualistChantingAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_cultist_ritualist_chanting_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtDashAction

[BtDashAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `max_duration` | [68](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L68) |
| `dash_speed` | [231](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L231) |
| `reached_destination_durations` | [282](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L282) |
| `start_move_rotation_timings` | [420](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L420) |
| `dash_direction_durations` | [432](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L432) |
| `dash_durations` | [449](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_dash_action.lua#L449) |

### BtDieAction

[BtDieAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `ragdoll_timings` | [63](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_die_action.lua#L63) |

### BtDisableAction

[BtDisableAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_disable_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtErraticFollowAction

[BtErraticFollowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `move_speed` | [29](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L29) |
| `rotation_speed` | [31](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L31) |
| `start_move_rotation_timings` | [172](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L172) |
| `start_move_event_anim_speed_durations` | [186](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L186) |
| `jump_durations` | [355](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_erratic_follow_action.lua#L355) |

### BtExitSpawnerAction

[BtExitSpawnerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `anim_driven_anim_event_durations` | [43](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_exit_spawner_action.lua#L43) |

### BtFlamerApproachAction

[BtFlamerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [24](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L24) |
| `min_move_duration` | [37](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L37) |
| `start_move_rotation_timings` | [110](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_approach_action.lua#L110) |

### BtFlamerCheckBackpackAction

[BtFlamerCheckBackpackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_flamer_check_backpack_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtGrenadierFollowAction

[BtGrenadierFollowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [33](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L33) |
| `skulking_vo_interval_t` | [44](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L44) |
| `check_grenade_trajectory_frequency` | [45](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L45) |
| `start_move_rotation_timings` | [310](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_follow_action.lua#L310) |

### BtGrenadierThrowAction

[BtGrenadierThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `throw_timings` | [87](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L87) |
| `action_durations` | [91](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L91) |
| `start_drop_grenade_timing` | [95](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L95) |
| `effect_template_timings` | [104](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L104) |
| `cooldown` | [176](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_grenadier_throw_action.lua#L176) |

### BtIdleAction

[BtIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_idle_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtInCoverAction

[BtInCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：[`MinionAttack.get_attack_delay`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L99)、[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L461)、[`MinionAttack.update_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L483)。

| 参数 | 首次读取行 |
| --- | --- |
| `enter_cover_durations` | [126](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L126) |
| `enter_cover_speed` | [160](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L160) |
| `suppressed_duration` | [190](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L190) |
| `peek_duration` | [294](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L294) |
| `aim_duration` | [390](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L390) |
| `start_aiming_at_target_timings` | [398](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_in_cover_action.lua#L398) |

### BtJumpAcrossAction

[BtJumpAcrossAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `blend_timings` | [36](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L36) |
| `rotation_duration` | [62](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L62) |
| `anim_timings` | [87](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_jump_across_action.lua#L87) |

### BtLeapAction

[BtLeapAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `start_movement_duration` | [77](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L77) |
| `start_leap_timing` | [78](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L78) |
| `aoe_bot_threat_duration` | [223](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L223) |
| `landing_duration` | [377](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L377) |
| `land_impact_timing` | [390](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_leap_action.lua#L390) |

### BtMeleeAttackAction

[BtMeleeAttackAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L1)。

直接属性词：[`melee_attack_speed`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L47)。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `assault_vo_interval_t` | [68](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L68) |
| `rotation_speed` | [84](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L84) |
| `push_enemies_frequency` | [99](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L99) |
| `attack_anim_durations` | [169](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L169) |
| `backstab_timing` | [184](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L184) |
| `attack_sweep_damage_timings` | [197](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L197) |
| `sweep_ground_impact_fx_timing` | [237](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L237) |
| `aoe_threat_timing` | [252](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L252) |
| `attack_anim_damage_timings` | [273](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L273) |
| `move_start_timings` | [354](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L354) |
| `animation_move_speed_configs` | [359](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L359) |
| `animation_move_speed_config` | [364](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L364) |
| `move_speed` | [376](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L376) |
| `ignore_animation_movement_speed` | [378](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L378) |
| `melee_attack_rotation_durations` | [383](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L383) |
| `effect_template_start_timings` | [394](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L394) |
| `aoe_threat_duration` | [517](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L517) |
| `rotate_towards_velocity_after_attack` | [742](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L742) |
| `move_speed_variable_lerp_speed` | [826](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L826) |
| `move_speed_variable_name` | [828](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L828) |
| `movement_speed_multiplier` | [840](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L840) |
| `catch_up_movementspeed` | [845](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action.lua#L845) |

### BtMeleeFollowTargetAction

[BtMeleeFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L1)。

直接属性词：[`movement_speed`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L31)。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `move_speed` | [50](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L50) |
| `rotation_speed` | [54](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L54) |
| `follow_vo_interval_t` | [68](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L68) |
| `running_stagger_duration` | [112](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L112) |
| `start_move_rotation_timings` | [274](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L274) |
| `start_move_event_anim_speed_durations` | [287](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L287) |
| `walk_speeds` | [388](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L388) |
| `walk_speed` | [390](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_melee_follow_target_action.lua#L390) |

### BtMinionVortexGrabbedAction

[BtMinionVortexGrabbedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `anim_durations` | [212](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_minion_vortex_grabbed_action.lua#L212) |

### BtMoveToCombatVectorAction

[BtMoveToCombatVectorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [34](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L34) |
| `running_stagger_duration` | [72](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L72) |
| `start_move_rotation_timings` | [154](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L154) |
| `start_move_event_anim_speed_durations` | [168](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_combat_vector_action.lua#L168) |

### BtMoveToCoverAction

[BtMoveToCoverAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `running_stagger_duration` | [69](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L69) |
| `start_move_rotation_timings` | [134](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L134) |
| `start_move_event_anim_speed_durations` | [148](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L148) |
| `speeds` | [154](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_cover_action.lua#L154) |

### BtMoveToPositionAction

[BtMoveToPositionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `enable_disable_locomotion_speed` | [33](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L33) |
| `adapt_speed` | [105](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L105) |
| `speed` | [186](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L186) |
| `start_move_rotation_timings` | [224](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L224) |
| `start_move_event_anim_speed_durations` | [238](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_move_to_position_action.lua#L238) |

### BtMutantChargerChargeAction

[BtMutantChargerChargeAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1)。

直接属性词：[`movement_speed`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1272)。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `min_time_navigating` | [204](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L204) |
| `navigating_rotation_speed` | [206](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L206) |
| `throw_timing` | [256](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L256) |
| `throw_duration` | [257](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L257) |
| `rotation_speed` | [260](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L260) |
| `min_time_spent_charging` | [272](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L272) |
| `charge_max_speed_at` | [283](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L283) |
| `animation_charge_speed` | [300](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L300) |
| `start_effect_timing` | [382](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L382) |
| `anim_driven_charge_anim_durations` | [394](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L394) |
| `start_rotation_timings` | [398](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L398) |
| `anim_move_speed_durations` | [403](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L403) |
| `start_colliding_with_players_timing` | [408](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L408) |
| `aoe_bot_threat_duration` | [428](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L428) |
| `dodge_rotation_speed` | [461](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L461) |
| `close_rotation_speed` | [461](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L461) |
| `miss_durations` | [475](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L475) |
| `wall_stun_time` | [653](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L653) |
| `smash_damage_timings` | [744](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L744) |
| `smash_anim_duration` | [807](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L807) |
| `after_throw_taunt_duration` | [892](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L892) |
| `grab_anim_duration` | [1067](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1067) |
| `push_minions_fx_cooldown` | [1189](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1189) |
| `charge_speed_min` | [1269](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1269) |
| `charge_speed_max` | [1280](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_mutant_charger_charge_action.lua#L1280) |

### BtOpenDoorAction

[BtOpenDoorAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_duration` | [42](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L42) |
| `open_door_time` | [76](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L76) |
| `open_door_time_offset` | [77](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_open_door_action.lua#L77) |

### BtPatrolAction

[BtPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_speed` | [81](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L81) |
| `durations` | [226](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L226) |
| `speeds` | [237](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_patrol_action.lua#L237) |

### BtPoxwalkerBomberApproachAction

[BtPoxwalkerBomberApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `move_speed` | [27](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L27) |
| `stagger_duration_modifier_during_lunge` | [64](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L64) |
| `fuse_timer` | [78](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L78) |
| `running_stagger_duration` | [140](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L140) |
| `start_move_rotation_timings` | [283](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L283) |
| `start_move_event_anim_speed_durations` | [296](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L296) |
| `walk_speeds` | [406](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L406) |
| `walk_speed` | [408](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L408) |
| `move_to_cooldown` | [462](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L462) |
| `lunge_duration` | [475](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L475) |
| `move_during_lunge_duration` | [476](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_poxwalker_bomber_approach_action.lua#L476) |

### BtQuickGrenadeThrowAction

[BtQuickGrenadeThrowAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `cooldown` | [67](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L67) |
| `throw_timing` | [105](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L105) |
| `action_durations` | [116](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L116) |
| `effect_template_timings` | [122](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L122) |
| `start_drop_grenade_timing` | [129](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_quick_grenade_throw_action.lua#L129) |

### BtRangedFollowTargetAction

[BtRangedFollowTargetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [33](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L33) |
| `running_stagger_duration` | [69](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L69) |
| `start_move_rotation_timings` | [121](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_ranged_follow_target_action.lua#L121) |

### BtReloadAction

[BtReloadAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_reload_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `anim_durations` | [28](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_reload_action.lua#L28) |

### BtRenegadeFlamerPatrolAction

[BtRenegadeFlamerPatrolAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_speed` | [125](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L125) |
| `end_durations` | [265](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L265) |
| `end_duration` | [272](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L272) |
| `durations` | [333](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L333) |
| `speeds` | [344](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L344) |
| `aim_duration` | [555](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L555) |
| `place_liquid_timing_speed` | [624](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L624) |
| `attack_duration` | [653](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_flamer_patrol_action.lua#L653) |

### BtRenegadeNetgunnerApproachAction

[BtRenegadeNetgunnerApproachAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `speed` | [29](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L29) |
| `rotation_speed` | [35](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_netgunner_approach_action.lua#L35) |

### BtRenegadeTwinCaptainDisappearAction

[BtRenegadeTwinCaptainDisappearAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `disappear_timings` | [18](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_disappear_action.lua#L18) |

### BtRenegadeTwinCaptainShieldDownAction

[BtRenegadeTwinCaptainShieldDownAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `regen_speed` | [107](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L107) |
| `stand_up_anim_duration` | [154](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L154) |
| `regenerate_full_delay` | [180](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L180) |
| `shield_break_duration` | [193](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_renegade_twin_captain_shield_down_action.lua#L193) |

### BtRunAwayAction

[BtRunAwayAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `run_speed` | [43](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L43) |
| `max_duration` | [66](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L66) |
| `push_nearby_players_frequency` | [76](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L76) |
| `speed` | [156](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L156) |
| `heal_frequency` | [217](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L217) |
| `start_move_rotation_timings` | [320](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L320) |
| `start_move_event_anim_speed_durations` | [334](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_away.lua#L334) |

### BtRunStopAndShootAction

[BtRunStopAndShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L103)、[`MinionAttack.update_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L107)。

| 参数 | 首次读取行 |
| --- | --- |
| `move_durations` | [94](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L94) |
| `action_duration` | [99](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L99) |
| `shoot_cooldown` | [115](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L115) |
| `blend_timings` | [142](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L142) |
| `start_move_rotation_timings` | [148](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_run_stop_and_shoot_action.lua#L148) |

### BtShootAction

[BtShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L1)。

直接属性词：[`minion_shoot_cooldown_modifier`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L720)。

共享射击／压制延迟调用：[`MinionAttack.get_attack_delay`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L350)、[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L388)、[`MinionAttack.update_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L419)。

| 参数 | 首次读取行 |
| --- | --- |
| `force_start_in_cooldown` | [60](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L60) |
| `shoot_cooldown` | [63](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L63) |
| `new_combat_vector_position_on_cooldown` | [78](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L78) |
| `not_allowed_cooldown` | [86](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L86) |
| `cooldown_anim_events` | [90](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L90) |
| `rotation_speed` | [101](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L101) |
| `exit_after_cooldown` | [204](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L204) |
| `start_move_rotation_timings` | [239](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L239) |
| `aim_duration` | [282](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L282) |
| `before_shoot_effect_template_timing` | [308](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L308) |
| `strafe_speed` | [498](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L498) |
| `strafe_speeds` | [603](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L603) |
| `cooldown_vo_event` | [754](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L754) |
| `update_game_object_shooting_cooldown` | [828](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_action.lua#L828) |

### BtShootLiquidBeamAction

[BtShootLiquidBeamAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L340)。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_speed` | [54](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L54) |
| `end_durations` | [170](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L170) |
| `aim_duration` | [209](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L209) |
| `place_liquid_timing_speed` | [360](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L360) |
| `aoe_bot_threat_timing` | [368](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L368) |
| `aoe_bot_threat_duration` | [410](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L410) |
| `sphere_cast_frequency` | [437](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L437) |
| `attack_duration` | [447](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L447) |
| `strafe_speed` | [866](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L866) |
| `strafe_speeds` | [956](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L956) |
| `exit_after_cooldown` | [995](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_liquid_beam_action.lua#L995) |

### BtShootNetAction

[BtShootNetAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `shoot_net_cooldown` | [83](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L83) |
| `aim_duration` | [149](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L149) |
| `aoe_bot_threat_timing` | [154](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L154) |
| `aoe_bot_threat_duration` | [172](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L172) |
| `net_speed` | [232](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L232) |
| `drag_anim_delay` | [344](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L344) |
| `drag_anim_exit_delay` | [382](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_net_action.lua#L382) |

### BtShootPositionAction

[BtShootPositionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：[`MinionAttack.get_attack_delay`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L197)、[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L229)、[`MinionAttack.update_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L252)。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_speed` | [40](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L40) |
| `start_move_rotation_timings` | [102](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L102) |
| `aim_duration` | [129](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L129) |
| `before_shoot_effect_template_timing` | [153](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_shoot_position_action.lua#L153) |

### BtSmashObstacleAction

[BtSmashObstacleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `rotation_duration` | [53](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L53) |
| `attack_anim_damage_timings` | [64](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L64) |
| `attack_anim_durations` | [66](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_smash_obstacle_action.lua#L66) |

### BtSniperMovementAction

[BtSniperMovementAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_movement_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `running_stagger_duration` | [88](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_movement_action.lua#L88) |
| `start_move_rotation_timings` | [150](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_movement_action.lua#L150) |
| `speeds` | [162](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_movement_action.lua#L162) |

### BtSniperShootAction

[BtSniperShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `reconsider_position_duration` | [122](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L122) |
| `lost_los_fail_duration` | [139](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L139) |
| `aim_duration` | [173](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L173) |
| `scope_reflection_timing_before_shooting` | [180](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L180) |
| `in_sight_duration_shoot_requirement` | [236](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L236) |
| `scope_reflection_timing_sfx` | [262](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L262) |
| `lock_to_target_lerp_speed` | [354](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L354) |
| `default_lerp_speed` | [355](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L355) |
| `time_per_shot` | [464](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L464) |
| `shoot_cooldown` | [489](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_sniper_shoot_action.lua#L489) |

### BtStaggerAction

[BtStaggerAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `stagger_duration_mods` | [110](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L110) |
| `ignore_extra_stagger_duration` | [121](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_stagger_action.lua#L121) |

### BtStepShootAction

[BtStepShootAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：[`MinionAttack.start_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L177)、[`MinionAttack.update_shooting`](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L183)。

| 参数 | 首次读取行 |
| --- | --- |
| `step_speed` | [159](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L159) |
| `step_anim_durations` | [167](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L167) |
| `step_move_timing` | [171](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L171) |
| `shoot_timing` | [175](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_step_shoot_action.lua#L175) |

### BtSummonMinionsAction

[BtSummonMinionsAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `shout_wwise_event_timing` | [33](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L33) |
| `initial_delay` | [49](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L49) |
| `stinger_delay` | [88](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L88) |
| `interval_til_next_summon` | [90](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_summon_minions_action.lua#L90) |

### BtSuppressedAction

[BtSuppressedAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `jump_durations` | [30](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L30) |
| `durations` | [30](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_suppressed_action.lua#L30) |

### BtSwitchWeaponAction

[BtSwitchWeaponAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_switch_weapon_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

没有提取到符合筛选规则的直接 action_data 字段。

### BtTeleportAction

[BtTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `min_wait_time` | [18](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L18) |
| `max_wait_time` | [19](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_teleport_action.lua#L19) |

### BtTwinCaptainDisappearIdleAction

[BtTwinCaptainDisappearIdleAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_disappear_idle_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `durations` | [32](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_disappear_idle_action.lua#L32) |
| `vo_trigger_timings` | [38](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_disappear_idle_action.lua#L38) |

### BtTwinCaptainIntroAction

[BtTwinCaptainIntroAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `duration` | [50](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L50) |
| `start_move_rotation_timings` | [190](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L190) |
| `start_move_event_anim_speed_durations` | [204](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L204) |
| `speeds` | [212](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_twin_captain_intro_action.lua#L212) |

### BtUseStimAction

[BtUseStimAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `duration` | [28](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L28) |
| `delay_timings` | [48](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_use_stim_action.lua#L48) |

### BtVoidShieldExplosionAction

[BtVoidShieldExplosionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `attack_anim_damage_timings` | [43](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L43) |
| `attack_anim_durations` | [49](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_void_shield_explosion_action.lua#L49) |

### BtWarpTeleportAction

[BtWarpTeleportAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_warp_teleport_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `teleport_timings` | [17](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_warp_teleport_action.lua#L17) |
| `teleport_finished_timings` | [202](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_warp_teleport_action.lua#L202) |

### BtWeaponMalfunctionAction

[BtWeaponMalfunctionAction](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L1)。

直接属性词：未发现本次筛选的 6 个速度／硬直属性。

共享射击／压制延迟调用：无。

| 参数 | 首次读取行 |
| --- | --- |
| `weapon_malfunction_time` | [51](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/nodes/actions/bt_weapon_malfunction_action.lua#L51) |

## 额外 TG 测试树

- [renegade_gunner_tg](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_gunner_tg_behavior_tree.lua#L1)
- [renegade_rifleman_tg](https://github.com/Aussiemon/Darktide-Source-Code/blob/0f0cb45991e9305ef4a7b925370792d7d6035f95/scripts/extension_systems/behavior/trees/renegade/renegade_rifleman_tg_behavior_tree.lua#L1)
