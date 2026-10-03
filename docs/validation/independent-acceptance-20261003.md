# Independent acceptance: compatibility plus minion stat gate

**Accepted for the reviewed source and selected regression scope. No concrete new defect found.** Compatibility commit: `9a3d0de6e0513e3a039e12a740e6d8298bb08a20`. Tested uncommitted `diy/diy_game.lua` SHA256: **`9A43E5CDA727810DEEF69997D86A8020430457913B678155BC2C3675D4133B6D`**. The main checkout still had that commit/hash and the same four dirty/untracked paths after review; `git diff --check` passed.

This supersedes the earlier review's unexecuted-test status for these selected cases. It does not claim full-suite or live-game acceptance.

## Independent execution evidence

After explicit approval to retain/use isolated Lupa 2.6, copied source/tests/docs into `acceptance-20261003-final/HavocConditionManager/` and ran existing tests there. All **457** copy/hash checks were stable. Snapshot manifest SHA256: `AD2AC9E8B83CBAE8271B53F6CAD660C408618086D239EC470BFB20D6F1312D9D`.

Used existing bundled Python 3.12.14, `D:/Projects/dev-support/test-runtime/lupa`, Lupa 2.6 / LuaJIT 2.1.1760617492, and explicitly pinned `DARKTIDE_SOURCE=D:/Projects/game-data/source`, clean native source HEAD `7e662fcda16219d775b84af50322be2e9cd9d62e`. Runtime import path was checked. Bytecode writes were disabled. Fresh logs, status JSON, benchmark output and temporary APPDATA stayed under the review copy. No installation, network, game, deployment, GPU work, source edit or global configuration change occurred.

| Existing check | Independent final exit code |
|---|---:|
| `syntax_tests.py` | 0 |
| `game_1_13_compat_tests.py` | 0 |
| `diy_minion_lifecycle_tests.py` | 0 |
| `native_replacement_loading_tests.py` | 0 |
| `condition_cleanup_tests.py` | 0 |
| `native_integration_tests.py` | 0 |
| `minion_stat_gate_tests.py`, plus its existing old/new comparison | 0 |

Final status index: `acceptance-20261003-final/accepted-test-status.json`, SHA256 `1AE8110E00978DBD20F165B1AA27345CBCA7AD4571696A7E25E371701B46FC73`. Per-test logs preserve actual stdout. Initial reviewer setup failures are retained: integration lacked Pillow under `-S`; it passed after explicitly adding the already installed bundled Pillow path. The first comparison's baseline Git read hit ownership protection; it passed using command-scoped `safe.directory`. No package was added and no global Git setting was changed. These were reviewer environment failures, not failing mod assertions.

Writer evidence was also inspected and frozen: its seven-check log SHA256 `29B291C3DF3118DDAA05231BF2B2ACB1DE13BA1E8154F81D71AEBEB97BD2CE54`, and comparison JSON SHA256 `6BF5CBC8BCB7F2402925C88ABBB1113A6176668F22C0307DA97C048405078F41`. Both remain unchanged in the main checkout.

## Gate semantics

The diff against the compatibility commit changes only the minion/player distinction in the stat callback: concrete player hooks pass `true` for client-effect lookup; concrete minion hooks pass `false` (`diy/diy_game.lua:481–509,531`). This uses the native class boundary even when breed metadata is absent. HCM's production `Network.effects` serves the local client player's unit exclusively (`diy/diy_network.lua:101–104`); minion callbacks previously performed those lookups but received no client effect.

The remaining authority/engine branch, native-only minion skip, effect-cache keys, effect application, proc callback, combat-time writes, provider/scoped update ownership and restoration are unchanged. No selection or RNG iteration was changed. The adapter adds no persistent identity or authority cache.

Independent old/new assertions passed for:

- Nil engine and native-only selections: 1000 native stat resets preserved; no DIY overlay introduced.
- Global/scoped minion overlays, including missing breed context and first scoped callback: one effect build at fixed clock and 1000 applications preserved; native stats/keywords retained.
- Host player, client local player, client remote player, client minion and absent Realms: player/client lookup and application outcomes retained; minions receive no player-only client effect.
- Engine/global/scope revision changes, clock advancement, explicit invalidation, engine finish/replacement, player respawn, character/session change, network timeout/finish, repeated require and omitted client callback. Fixture reload coverage remains mocked.

The real-native lifecycle tests also passed with the gate: deletion/cleanup, provider ownership, native buff removal, mission reuse, first proc and independent pause/registration reconciliation. **The prior P2 is now closed with executable regression evidence**, within the harness's modeled native construction/registration boundary.

Compatibility checks passed for current/legacy difficulty labels and colors; forced roamer faction/trailing arguments/returns; native resource ability adaptation; pacing prepared identity/replacement, heat transitions and deferred monsters; readiness/activation/deferred spawning and original listener ownership; standalone integration/UI behavior. They use native data/method bodies with explicit construction, navigation, package and event fixtures. This is meaningful targeted evidence, not a full running engine.

## Same-workload benchmark verification

Baseline source SHA256 is `C3DBC6EC58069BE9EFA59FD98CAF1C9C6DCD90FAD31D7435BA0432883D89E160`, read directly from compatibility commit `9a3d0de6e0513e3a039e12a740e6d8298bb08a20`. Candidate source matches the accepted `9A43...3B6D` hash. Both sources were hash-asserted before replay. Their source diff contains only the gate/wiring above; the helper uses identical Engine/Network code, fixture, selection, native-reset stub and fixed engine clock for both versions.

Each timing batch performs **1000 native stat resets plus HCM callbacks**, on one fixed minion, after 500 warm-up callbacks; 30 samples alternate old/new order. Instrumentation is disabled for timed batches. The semantic comparison asserts equal native/apply/effects/authority/engine counts before and after. Across the seven minion cases, client-effect/context/character probes drop from 1000 to zero and local-player lookups from 2000 to zero; the three player cases retain their previous probes.

Fresh independent comparison: `acceptance-20261003-final/HavocConditionManager/build/checks/minion-stat-gate-comparison.json`, SHA256 `6D6F85AE41D7860C5C821AA886FF4C4CFC49FADB3ECA9E40FD3DC9F69FBF6CE4`.

| Mocked case | Before median, ms/1000 callbacks | After median, ms/1000 callbacks |
|---|---:|---:|
| Nil engine | 0.1240 | 0.1079 |
| Native-only selection | 0.1938 | 0.1728 |
| Active passive overlay | 0.2753 | 0.2462 |

The writer's separate run has matching source pins and operation-count behavior. Timing differences between runs are expected. These numbers are **callback microbenchmarks**, not game frame times, FPS improvement, total allocation counts or an explanation of the user's sustained FPS loss. The fixed-clock cache workload excludes ongoing DIY ticks and changing conditions. Heap-growth observations are limited to this mocked batch.

## Selected installed-source correspondence

Independently inspected `D:/Projects/HCM_SOURCE_CORRESPONDENCE_20261003.md` (SHA256 `6174B472C10B52E5BDE942A804DDB15740B63D19999174E5251DCD2681B2A8CE`), fresh extraction manifest (`8F04576FAB0A9B940605B1FCD9E1B5259DA48D7E6AA49908D75F76964C1207CA`) and module comparison (`B8C0D59D312AF445253196A66A65C38A3C894059093F4B84800D36D8E4C968DF`). The manifest records the actual installed bundle path, exact 14-name dictionary, one-thread extraction/decompilation arguments, output paths and tool identities; completion records both have exit zero. Extraction log reports 14 outputs at 16:55 UTC. The prior Studio cache is not used as this build's evidence.

Current Steam manifest still reports build `25606770`, the same three depot manifests, and executable version `1.3.802.934`. Rehashed the installed database/executable/Oodle inputs and both existing tool executables: all match the before/after manifest hashes. Decompiler hash also matches its existing build-info file for source commit `166658ffe9eaf64e94887cd8df9d9340f695d9a9`. Rehashed all 14 bytecode, decoded and public files: all match the comparison record. The gate hash remains frozen. Structured checks: `acceptance-20261003-final/correspondence-file-checks.json`, SHA256 `EA4F1E6556001305ECF7946C5DC5658CE8BC8843647DF6CABC8A48F776E40565`.

Read the pinned existing lexer at `game_bundle_audit.py:51–102`, then independently reran **only its AST-isolated pure token function**, without importing the Studio audit or rerunning tools/Lua. Result: **14/14 token matches**, zero mismatches. Quoted and long-bracket strings are retained as raw tokens; identifiers/numerical text are not renamed or converted. It discards comments and whitespace outside strings, then only commas immediately before `}`. Comparing a strict token view confirmed the latter removes 75 public-source final table commas and zero decoded commas. Those are optional Lua table separators; no other post-lexer token removal occurred. Recheck: `acceptance-20261003-final/correspondence-token-recheck.json`, SHA256 `CA95492815F4FF2271C64A1033F851B74440A17C4C499547BCB103ABB5C7694C`.

This closes the source-version gap for the **14 selected API/lifecycle modules** at the recorded current installation. It establishes decompiled-token correspondence, not raw-source identity, independently proven decompiler correctness, whole-game bundle integrity or which code is loaded after other mods hook it. Unexamined modules remain outside the result.

## Remaining boundaries

Live DMF reload/unload, mission/UI integration in the running game and matched ordinary-condition performance are not validated. The full external-fixture suite was not run. Delayed-package derived-mutator and unequal shared-pool charge-cost coverage remain limited as documented. No deployment or game installation was changed.

The gate is a narrowly supported removal of unnecessary minion network probes. Authority/engine upkeep and the other ordinary-path cost hypotheses in the earlier performance audit remain separate profiling work.
