# Custom Emperor's Fading Light III/IV milestone

This is a separate local feature milestone on `feature/custom-efl-four-tiers`, based on independently accepted rank50/P2 checkpoint `17851628cc9ae8de03ccf4a13c06222fe61f38f2`. Native I/II and rank1–50 behavior remain covered by the existing tests. III/IV are HCM balance choices, not native game facts. This checkpoint is for independent review; no archive, installed-mod change, game launch or release was performed.

## Native evidence and authorized extension

Host: DESKTOP-R573TA1. Installed Darktide executable: PE `1.3.802.934`, Steam build `25606770`. Source checkout: `D:/Projects/game-data/source`, native1.13.1 commit `7e662fcda16219d775b84af50322be2e9cd9d62e`. The15-module rank50 report covers none of the nine EFL definition/consumer files. As the [independent review](../../HavocConditionManager-review/efl-four-tiers-20261003/independent-final-review.md) established, installed correspondence for SpecialsPacing/MonsterPacing/HordePacing comes from `D:/Projects/game-data/hcm-suite-source-20261003-verified/report.json`; PacingManager comes from `D:/Projects/game-data/hcm-installed-source-20261003`. Those four hash triples were rechecked by that reviewer. The three definition files and MutatorModifyPacing/MutatorHordePacingOverrides previously had only pinned public-source evidence. The bounded [five-module backfill](validation/efl-source5-20261003.json) now confirms their installed bytecode/decoded/public token correspondence using the same pinned tools, with executable/database/Oodle and public inputs unchanged before/after. It covers exactly `havoc_circumstance_template.lua`, `mutator_modify_pacing_templates.lua`, `mutator_horde_pacing_template.lua`, `mutator_modify_pacing.lua` and `mutator_horde_pacing_overrides.lua`; no broader installed coverage is inferred. These source/executable identifiers are separate; DMF's exact runtime version remains unconfirmed. Tests use approved Python3.12.14/Lupa2.6/LuaJIT2.1 and the pinned SoloPlay2.6.5/actual HED3.2.0 fixtures. No dependency was installed.

Native circumstances are `mutator_increased_difficulty` (I) and `mutator_highest_difficulty` (II), from `scripts/settings/circumstance/templates/havoc_circumstance_template.lua:190/211`. III/IV use the complete native II bundle. They alter only the following four pacing paths:

| Pacing value | Native I | Native II | Custom III | Custom IV |
|---|---:|---:|---:|---:|
| Captain travel range | 240–360 | 120–240 | 60–160 | 30–106.6666667 |
| Eligible special-slot monster chance | .05 | .10 | .20 | .40 |
| Monster cooldown range, seconds | 550–600 | 450–500 | 368.1818182–416.6666667 | 301.2396694–347.2222222 |
| Horde timer range, seconds | 140–240 | 100–200 | 71.4285714–166.6666667 | 51.0204082–138.8888889 |

Each component is calculated at runtime as `II * (II / I)^(tier - 2)` from native anchors; the displayed decimals are rounded only for this table. Captain/monster values are in `mutator_modify_pacing_templates.lua:144/157/182/205`; horde ranges are in `mutator_horde_pacing_template.lua:224/637`. Existing coarse/fine edits are compiled first, then multiplied by the same native ratio. Probability is capped at1 for composed user edits; a zero user value remains zero. No HP, regeneration, grace period or concurrency is extrapolated. II's110 minions, seven-second wave interval, one monster replacement slot, three monster breeds, `.4` HP factors, resistance+1, auric/twin/stagger/spawn-type/terror-event rules and native eligibility remain unchanged unless independently changed by existing user controls.

## Storage, UI and persistence

The existing difficulty dropdown offers None and exclusive I/II/III/IV. Its default remains I. III/IV labels explicitly say custom in English, Simplified and Traditional Chinese. UI IDs `hcm_efl_3/4` are local choices only; no native template or network lookup entries are created. SoloPlay stores I's native identity for I and II's identity for II–IV. III/IV metadata is a strict HCM-owned `{version=1,tier=3|4,native_id="mutator_highest_difficulty"}` record under `hcm_custom_efl_v1`. Malformed records reject instead of being guessed or silently normalized. A direct native setting write, including the same II value, invalidates stale custom metadata.

Changing the rank slider preserves the chosen EFL tier, including ranks40/50. Explicit Randomize keeps the native generator's behavior and replaces III/IV with its generated None/I/II. No rank threshold selects custom III/IV automatically. Primary conditions remain separate; launch data contains exactly one native II for III/IV, with no I/custom UI IDs alongside it.

The existing HCM HED bridge carries a separate optional `hcm_custom_efl_v1` document field, even at rank16/40. The original native codec validates the stripped document and its native II context before owned metadata is reattached. Rank50 and EFL fields can coexist. Legacy documents remain readable without changing current selection; explicitly applying one clears custom EFL. Separate `hcm_custom_efl_modes_v1` HCM/HED slots preserve selections independently of custom rank. Transactions include both owned keys, existing cached settings, SoloPlay values and UI state. Failures after native/owned/mode writes restore the previous complete state. Existing late API appearance/replacement/idempotency and third-party ownership handling are preserved. No external HED files are changed.

## Runtime ownership and cleanup

Launch metadata is retained in MechanismBase's local context and matched to native mission data, supported mission, parsed rank/circumstance and actual SoloPlay/local authority. It is independent of custom-rank metadata. Neither backend identity nor RPC data is extended.

`template_runtime.prepare` privately extends only three recognized native II roots after coarse/fine compilation. Captain ranges reach `MutatorModifyPacing.on_gameplay_post_init` → `PacingManager.add_pacing_modifiers` → `MonsterPacing.fill_spawns_by_travel_distance`. Monster chance/cooldown reach `MutatorModifyPacing.init` → `SpecialsPacing.set_monster_spawn_config`. Horde ranges reach the existing override getter before `HordePacing.on_gameplay_post_init` draws its first interval. This works before the mutator manager is published. All final branches are marked prepared, and root condition gates follow the final clone. Default EFL-only preparation skips unrelated roots and the coarse compiler. No duplicate DMF hook is added.

The mission retains its launched custom tier for III↔IV selection changes; those changes take effect next mission. As required by this milestone, choosing None/I/II explicitly retires the four overrides in the active mission. Disable, unload and mission exit also restore the owned fields in place to their compiled pre-EFL baseline. Ownership checks preserve intervening foreign field replacements. Retiring EFL invalidates its compiler cache without discarding unrelated frozen coarse/fine settings, gates or prepared identities. Entering GameplayStateRun preserves copies already created in GameplayStateInit.

Native deadlines, current waves/slots and already built captain plans remain owned by the game. Cleanup changes subsequent draws; it does not undo spawned actors or rebuild captain plans from the map start, which could recreate passed points. A retired mission owner cannot reacquire custom metadata. New mission owners receive fresh snapshots and copies. Reload/unload deactivates buried old setting observers while retaining third-party wrappers.

## Verification and measured workload

The complete canonical suite passes40/40 with ordered integer-zero exits and identical pre/post source/test/tool hashes. The original37 case scripts and existing rank50/P2 test script are unchanged. The new EFL case reuses the current native/installed-mod harness. It covers all ranks1–50 × tiersI–IV; exact native-derived curves; I/II reference/structure identity; four-path-only changes; ranges/probability; finite/invalid metadata; multiplayer/client/unsupported-map/context gates; real native init/post-init, captain plan, horde first/subsequent draws and monster slot/cooldown consumers; Init→Run; coarse/fine composition; fine encounter gates before/after cleanup; reopen/default/manual/Randomize; actual HED codec/presets/capture/modes/late APIs/rollback; and disable/mission/reload/unload/foreign ownership.

Read-only implementation review identified three interactions now fixed and covered: transfer root encounter gates to the final horde clone; retire EFL without clearing unrelated compiler state; preserve Init-created copies when entering Run. Follow-up review found no remaining concrete runtime/preset blocker. The final test refresh additionally executes the real dropdown activation callback, constructs25 fresh view objects with the actual constructor, tests captured HED wrappers after disable/unload, and forces a`.01` occupied-slot probe so all four tiers reach the native slot-cap/cooldown branch. Full-result SHA256: `865f4f6505fdd63d7928f871c9d32dd06df24a8757749342bb83adb54ed11a1f`;328 source and66 test/tool hashes match the current evidence gate.

With default coarse/fine settings, three fresh II roots create exactly three custom copies. Another30,000 calls reuse them, with zero coarse compiler calls. No per-frame/per-entity hook, logging or whole-table scan is added for EFL. This is an offline call-count result, not a frame-time measurement.

Same-input native callback workload: one3600m route with180 captain points at20m spacing;3600 one-second special-slot checks;3600s horde horizon. Range draws use midpoints, choices use the first index, probability draw is fixed at`.15`, and no terror event/occupied monster slot occurs except the explicit cap assertion.

| Tier | Captain plan points | Horde schedules within horizon | Horde timer draws | Monster replacement candidates | Slot checks |
|---|---:|---:|---:|---:|---:|
| I | 12 | 19 | 20 | 0 | 3600 |
| II | 20 | 24 | 25 | 0 | 3600 |
| III | 30 | 30 | 31 | 10 | 3600 |
| IV | 45 | 38 | 39 | 12 | 3600 |

These are deterministic scheduling candidates, not actual spawns or expected random gameplay averages. Shorter timers and greater chance increase potential game workload: relative to II, the fixture has50%/125% more captain plan points and25%/58.3% more horde schedules for III/IV. The fixed`.15` chance deliberately distinguishes native I/II refusal from III/IV acceptance; their zero candidate count is not a gameplay rate claim. Native cap/cooldown still execute. Physics/navigation/rendering/actors and real allocations/frame times are outside this harness. No FPS improvement is claimed.

Evidence is in [full suite results](validation/efl-four-tiers-full-suite-result-20261003.json), [per-case log](validation/efl-four-tiers-full-suite-20261003.txt), [workload/call counts and native consumer hashes](validation/efl-four-tiers-workload-20261003.json) and [current-source gate/archive preservation](validation/efl-four-tiers-evidence-gate-20261003.json). Old rank50/P2 evidence and test.1/test.2 ZIPs remain unchanged. External source/installed-mod fixtures are pinned separately; they remain outside the runner's pre/post input maps.

Live game UI/rendering, real disk persistence, DMF reload, gameplay and frame-time validation are unperformed. The reviewed feature checkpoint stopped before packaging, deployment or game testing. After independent acceptance and the provenance correction, [4.6.0-test.1 candidate preparation](local-candidate-4.6.0-test.1-20261003.md) records the fresh full suite and runtime-only archive separately; the original milestone evidence above is preserved.
