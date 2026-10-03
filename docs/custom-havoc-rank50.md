# Custom Havoc ranks through 50 — implementation milestone

Implemented on branch `feature/custom-havoc-rank50`, based on accepted offline candidate commit `61ab522`. Core adapter/UI: `0ab1818`; presets/lifecycle/native consumers: `4ac25d7`; complete evidence gate: `db1c412`. EFL III/IV remain unimplemented and require a separate commit after this milestone's review.

## Scope and source identity

The actual mod is `D:ProjectsHavocConditionManager`; the optional adapter is implemented here, without editing HED, HavocDirectorStudio or HavocEventDirector. Installed Darktide: Steam app1361210/build25606770, executable1.3.802.934. Native source: clean `D:Projectsgame-datasource` commit7e662fcda16219d775b84af50322be2e9cd9d62e (1.13.1). Fifteen rank-relevant modules match installed extraction: [extraction report](../../game-data/hcm-rank50-source-20261003/report.json). Installed SoloPlay2.6.5 source and HED3.2.0 fixtures are reused read-only. The installed DMF runtime version remains unconfirmed; staging package dates are not runtime-version evidence.

The [earlier numerical audit](../../HavocConditionManager-review/havoc-50-numeric-audit-20261003.json) remains unchanged as historical read-only evidence. Its then-hypothetical continuation was subsequently authorized for this implementation. This document records that later implementation.

## Formula and native contracts

For a selected ordinary modifier field, with `d = requested_rank - 40`:

`custom_value = native_value_of_selected_tier + d * (value_last_tier - value_previous_tier) / (rank_last_attainment - rank_previous_attainment)`.

The attainment ranks come from the actual native40-row config, and values from actual settings/BuffTemplates. The slope is calculated once per loaded rules module; the selected tier remains the anchor. An off modifier stays off; positive modifiers and existing EFL I/II definitions remain unchanged. Native tiers/IDs/global tables are not extended or edited. No generic spawn multiplier or arbitrary reduction is applied.

These formulas show the full native40-selected ordinary profile. Numeric comparisons are exact formulas, with decimals rounded to six places.

| Quantity | Formula at custom41–50 | 40 | 41 | 45 | 50 |
|---|---|---:|---:|---:|---:|
| Player HP factor | .65−d/60 | .650000 | .633333 | .566667 | .483333 |
| Player toughness flat | −45−5d/9 | −45.000000 | −45.555556 | −47.777778 | −50.555556 |
| Toughness regen factor | .5−d/90 | .500000 | .488889 | .444444 | .388889 |
| Ammo pickup factor | .4−d/120 | .400000 | .391667 | .358333 | .316667 |
| Elite HP factor | 1.5+d/40 | 1.500000 | 1.525000 | 1.625000 | 1.750000 |
| Special HP factor | 1.5+d/48 | 1.500000 | 1.520833 | 1.604167 | 1.708333 |
| Monster HP factor | 1.7+.03d | 1.700000 | 1.730000 | 1.850000 | 2.000000 |
| Horde HP factor | 1.3+.005d | 1.300000 | 1.305000 | 1.325000 | 1.350000 |
| Horde hit mass factor | 2.7+.02d | 2.700000 | 2.720000 | 2.800000 | 2.900000 |
| Melee power factor | 1.5+d/40 | 1.500000 | 1.525000 | 1.625000 | 1.750000 |
| Horde rate factor | 2.4+.04d | 2.400000 | 2.440000 | 2.600000 | 2.800000 |
| Terror point factor | 1.85+d/32 | 1.850000 | 1.881250 | 2.006250 | 2.162500 |
| Special capacity bonus | 6+.1d | 6.000000 | 6.100000 | 6.500000 | 7.000000 |
| Monster encounter bonus | 3 | 3 | 3 | 3 | 3 |
| Elite density bonus | 1+.125d | 1.000000 | 1.125000 | 1.625000 | 2.250000 |
| Ogryn density bonus | .8+.05d | .800000 | .850000 | 1.050000 | 1.300000 |
| Melee attack speed factor | 2+.05d | 2.000000 | 2.050000 | 2.250000 | 2.500000 |
| Ranged attack speed factor | 1.3+.01d | 1.300000 | 1.310000 | 1.350000 | 1.400000 |
| Ranged shots factor | 2.25+.05d | 2.250000 | 2.300000 | 2.500000 | 2.750000 |
| Permanent damage ratio | .3+d/160 | .300000 | .306250 | .331250 | .362500 |
| Vent factor | 1.85+d/60 | 1.850000 | 1.866667 | 1.933333 | 2.016667 |

The GME terror setter passes raw .85+d/32; the native manager adds1. Its full factor is shown above. HP/regen values likewise include their native additive base1. Capacity/density bonuses remain fractional until their native consumers quantize actual counts. On a native integer special-slot base5, `ceil(5+bonus)` is11/12/12/12. No pre-rounding or new concurrency policy is added. With no other maximum buffs, actual player toughness is `ceil(B−45−5d/9)`: B75 gives30/30/28/25; B125 gives80/80/78/75. Existing additive/multiplicative buffs continue to combine through the native Buff class.

Requested rank41–50 is HCM-owned local metadata. Native serialized Havoc rank, native current rank, challenge and resistance retain their rank40 identity. This keeps Tough Skin's ranged damage-taken coefficient at.5 and retains the native Spillway exact-rank40 twin eligibility, including its existing chance gate and spawn requirements. Other raw-rank consumers remain at40. Ordinary selected values above continue beyond40. Official backend progression/rewards/matchmaking and RPC contracts are not changed.

Runtime extension requires SoloPlay's `HOST_TYPES.singleplay` mode and local authority. Training grounds/shooting range are rejected. The native launch context is parsed and matched against the mechanism's actual retained context; no global pending launch value can spill into another mission. A deep mission snapshot is frozen by difficulty owner and cleared on mission boundaries/unload. Mid-mission setting changes affect the next mission.

## Implementation and persistence

- `custom_havoc_rank.lua`: finite integer1–50 validation; strict owned records/presets/mode slots; explicit18-modifier field list; selected-tier curves, scalar deltas and immutable cached Buff clones.
- `custom_havoc_rank_runtime.lua`: bounded native generation, separate launch metadata, verified singleplay session, scoped native Buff initialization, snapshot invalidation and ownership-safe setter observer.
- `custom_havoc_rank_presets.lua`: optional adapters around actual HED codec/capture/apply/Studio/mode functions; selected tiers, zeros and lock state survive JSON/preset/mode roundtrips. Legacy documents remain readable; applying an old native-rank40 preset or writing the same native40 value clears stale custom rank metadata and dirties Studio.
- Entry point, actual view callbacks/settings and three localizations use the same rank API. Native1–40 generation stays byte-equivalent for the same tested seed/RNG boundary. Changing rank preserves manual selections; explicit Randomize retains the native reset behavior.

Preset/mode transactions restore native settings, HED cached configuration, DIY cached options, seeds, contexts, mode slots, mission/rank, modifier/lock choices and view state when a write fails. Ordinary busy/disabled/invalid-mode refusal delegates directly, without running rollback or disturbing active owners. Captured adapters become inactive on unload/API replacement, and third-party wrapper ownership is preserved.

DMF source confirms `on_unload(exit_game)` runs before hook cleanup, both for reload(false) and exit(true), and includes disabled mods. The callback gets the boolean only. No separate mod on_reload callback is assumed. [Existing installed DMF evidence](validation/installed-dmf-evidence-20261003.json) records loader/manager identities; events.lua SHA256 is244231F05B832BBB8C66FA67B15109C9F8D943213BF4A2C44282A8F0FFACFF68. Lifecycle tests execute the actual HCM callback with DMF hook removal as an explicit boundary; DMF itself was not run.

## Validation and limits

The complete runner preserves all prior37 cases and adds the custom-rank and suite-evidence cases, for39. Evidence is copied to [full result](validation/rank50-full-suite-result-20261003.json), [full log](validation/rank50-full-suite-20261003.txt) and [native consumers40–50](validation/rank50-native-consumers-20261003.json). Python3.12.14, preapproved Lupa2.6/LuaJIT2.1.1760617492; sequential modest-CPU execution.

Rank tests execute actual native generators/parser, modifier initialization/server setters, Buff.init/stat accumulation, HP/toughness consumers, Spillway force-push phase eligibility/chance, actual HCM rank/UI callbacks, and actual installed HED config/codec/preset/mode/capture functions. Engine rendering, VO, unit creation, spawn transport, JSON transport and DMF hook cleanup are explicit boundaries. They cover all41–50 selected ordinary scalar/stat fields; lower selected tiers, zeros, immutable definitions, independent DIY same-name buffs, snapshot changes, malformed values, failed native/owned/mode writes, whole-state/UI rollback, reload/unload/disable and absent/replaced optional APIs.

The initial full run had two existing Git-ownership read failures (37/39 passed); the next runs use process-local safe.directory for this exact verified source repository. No global Git configuration was changed. A temporary expanded assertion incorrectly expected the final terror factor at the raw setter boundary; it was corrected to its source-defined raw .85+d/32 before the final run.

The runner now records the complete required/requested lists and every exit code, source hashes before AND after, and test/package-code hashes before AND after. Packaging independently reads the current required manifest, requires exactly one zero exit per case and checks both snapshots against current bytes. Eight malformed/stale evidence cases are rejected. The gate is validated without constructing a new archive. Final full-result SHA256: `1e1ea9bda05eefa904777980f72596b6c6bf769f18e0eee69be3d88045452b5c`. This freshness scope covers packaged source, Python test files and three package tools; it does not pre/post-hash external game/HED fixtures. Their separately recorded source identities and SoloPlay's pinned fixture hashes provide provenance.

No game was launched and no installed mod/settings were changed. Gameplay frame times, real multiplayer synchronization, mission loading/rendering, reload in the real DMF and real boss spawning remain unperformed. These tests establish offline compatibility behavior, not FPS improvements. New work adds mission/initialization/spawn/Buff-boundary work with cached curves/templates; no new per-frame update or whole-unit scan was introduced. Existing performance evidence remains separate in [compatibility report](game-1.13-compatibility.md).

Accepted4.5.1-test.2 and test.1 archives, historical reports, source version and installed mod are unchanged. No new archive, dependency, release, publication or push. EFL III/IV are the next separately reviewed feature slice.
