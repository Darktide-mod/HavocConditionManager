# HCM native source correspondence — 2026-10-03

Outcome: **14/14 selected installed-bundle Lua modules match public 1.13.1 commit `7e662fcda16219d775b84af50322be2e9cd9d62e` by the existing Lua token comparator; zero mismatches or missing outputs.** This is an offline, module-scoped result, not whole-game/live compatibility acceptance.

The original nearby sources were community Git checkouts, not proof of installed code: `D:/Projects/game-data/source` is the public 1.13.1 checkout; `D:/ModProject/.references/darktide-source-1.12.5` and Studio's `game-data/source` are public 1.12.5 `0f0cb45991e9305ef4a7b925370792d7d6035f95` checkouts. Studio's existing `game-data/index/game-bundle-audit.json` recorded a 269-module match, but its input executable and bundle-database hashes differ from the current installation. That cached result cannot certify this build; it also lacks most changed lifecycle modules.

Current installed metadata: Steam build `25606770`, executable file version `1.3.802.934`. Depot manifests: 1361211=`2981460983667067232`, 1361212=`7488139965064667169`, 1361213=`5456051176845852840`. Executable version is a PE version, not a marketing-version assertion.

Current input SHA256 hashes, unchanged before/after the bounded extraction:

| Input | SHA256 |
|---|---|
| `bundle/bundle_database.data` | `36DA6AC68790E64F02A1653EBE6D47C1BCE309F71FF2D86EA8C1ED63C422EB31` |
| `binaries/Darktide.exe` | `28B843BC2905FAAA0F27329D68E5DE989DF908F2552D80BF2B3C79B86E259775` |
| `binaries/oo2core_9_win64.dll` | `8595A4795F1E0C7F548598F3E2AA528B6BE5456C6D934C665182EAECB04156C0` |

Existing recognized tools were reused in place from Studio's `tools` directory; none installed or modified. limn's folder is named `0.7.2`, but its help actually reports `0.7.1`; the executable hash is `03EA9AD220E3D217414362B365ACC64B0E47A37ADAF7CF5F478B0C68C6A5EC67`, equal to the prior audit record. The existing decompiler hash is `FF56EE49320A609CCB5357B8C4EC0578EBC67A14546FADAE1A3D9BFE2E014D88`, equal to its build-info manifest, which identifies Aussiemon/luajit-decompiler-v2 commit `166658ffe9eaf64e94887cd8df9d9340f695d9a9`.

limn read the installed `F:/SteamLibrary/steamapps/common/Warhammer 40,000 DARKTIDE/bundle` with a 14-name dictionary and one CPU thread. It completed successfully in 6.744 seconds and produced the 14 requested files. The decompiler completed with exit zero; all outputs were individually checked for existence and nonzero length. No game Lua was executed. Output is retained only under `D:/Projects/game-data/hcm-installed-source-20261003`.

Compared modules:

- `scripts/settings/difficulty/danger_settings.lua`
- `scripts/managers/pacing/pacing_manager.lua`
- `scripts/managers/pacing/roamer_pacing/roamer_pacing.lua`
- `scripts/managers/pacing/heat_pacing/heat_pacing.lua`
- `scripts/foundation/managers/extension/extension_system_base.lua`
- `scripts/extension_systems/buff/buff_extension_base.lua`
- `scripts/extension_systems/buff/minion_buff_extension.lua`
- `scripts/extension_systems/buff/player_unit_buff_extension.lua`
- `scripts/extension_systems/ability/player_unit_ability_extension.lua`
- `scripts/managers/mutator/mutator_manager.lua`
- `scripts/managers/mutator/mutators/mutator_base.lua`
- `scripts/managers/mutator/mutators/mutator_stimmed_minions.lua`
- `scripts/managers/mutator/mutators/mutator_spawner.lua`
- `scripts/game_states/game/gameplay_sub_states/gameplay_init_step_states/gameplay_init_step_managers.lua`

The previously inspected pure `lua_tokens` function from Studio's existing `scripts/game_bundle_audit.py` was isolated using Python AST; the Studio audit module was not imported/executed and its cache was not changed. This comparison ignores comments, spacing and optional final table commas, while preserving identifiers and string contents. Raw SHA256/text differs, principally due to formatting/trailing commas; all token sequences match. Raw bytecode, decoded text, public-source and token hashes are recorded per module. This does not assert arbitrary behavioral equivalence or byte-identical Lua source.

Evidence directory contains `modules.txt`, `dictionary.txt`, `bytecode/`, `decoded/`, extraction/decompilation logs and exit records, `input-before.json`, `input-after.json`, `module-hashes.json`, `module-comparison.json` and `manifest.json`. Manifest SHA256: `8F04576FAB0A9B940605B1FCD9E1B5259DA48D7E6AA49908D75F76964C1207CA`; comparison SHA256: `B8C0D59D312AF445253196A66A65C38A3C894059093F4B84800D36D8E4C968DF`. Exact commands/tool paths are in the manifest.

No mod/Studio source, installed game, anti-cheat/security, network behavior or deployment was changed. Repair source remained frozen; gate `diy_game.lua` SHA256 is still `9A43E5CDA727810DEEF69997D86A8020430457913B678155BC2C3675D4133B6D`. Public source checkout remains clean. Git HEAD remains compatibility commit `9a3d0de`; gate/test/docs working-tree state is unchanged and awaits independent gate review before commit.

The installed-bundle correspondence gap is closed for these selected native API/lifecycle modules. It remains open for unexamined modules and for actual loaded runtime behavior, optional mod/hook interactions, DMF reload, UI, settings/mission transitions and gameplay frame times. No full compatibility guarantee or FPS result is inferred. The smallest remaining live step, after separately authorized deployment/launch, is a controlled local test of these transitions plus same-scene disabled/enabled frame timing; this pass performed neither.
