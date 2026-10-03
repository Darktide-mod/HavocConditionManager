# Full-suite closure — 2026-10-03

The complete 37-script offline suite passes against current public game source `7e662fcda16219d775b84af50322be2e9cd9d62e` (1.13.1), with the existing approved Python 3.12.14/Lupa 2.6 LuaJIT runtime. Both `tests/run.py --keep-going` and the unfiltered default entry point pass. No assertions or cases were removed and no failures were skipped. The initial non-stopping run recorded 25 passes and all 12 failures.

## Diagnosed failures and repairs

| Failed scripts | Confirmed cause | Repair and retained coverage |
| --- | --- | --- |
| native_template, native_elite_balance, native_straggler | Test parser dropped new `[breed_tags.name] = true` assignments. Native enum values remain strings. | Support bracketed and old literal assignments in both harnesses; evaluate all 59 current native tag blocks independently in Lua. Keep coarse-consumer, category-growth and protected-enemy assertions. Actual native horde/patrol fixtures retain common counts and double elite counts. `elite_density` has 3,161 consumers. |
| native_runtime, native_special_pressure | Fixtures omitted the new native effective-special-slot helper and constructor bonus multiplier. | Execute the real native helper with constructor value 1; verify effective slots and a reduced bonus without rescaling the template. |
| native_encounter_location | Native monster allowance now checks active heat; fixture omitted that method. | Preserve active allowance/full-cap assertions; add inactive-heat refusal before allowance work. |
| diy_medical_map | Hardcoded old checkout paths fail after relocation; pickup fixture supplied obsolete method name. | Use shared configurable game/source paths and the actual packaged No healing condition. Match current `despawn_item_unit`; retain native medical, player-transfer, authority, cleanup and mission tests. |
| native_ui, diy_package_page | Optional HED source was assumed adjacent. | Configure the source root and load the unchanged actual HED 3.2.0 source copied read-only from its existing installation. Keep every cross-mod UI assertion. Separate native integration still checks HED absent and four standalone pages. |
| native_intensity_profile, release_debug, archive_guard | Sparse checkout omitted tracked immutable ZIP/publishing fixtures; prior candidate version had not updated omitted publishing metadata. | Restore exact existing Git objects for 3.4.0/4.4.9 ZIPs and six publishing files. Align local test metadata and Optional Files category. Preserve independent migration, archive and release-format assertions. No publishing operation performed. |

The original 4.5.0 source reproducing the elite assertion was evidence of a pre-existing test failure, not evidence that it was harmless. Source tracing now establishes that the native tags and composition consumers remain compatible; no runtime classifier patch was needed. Hordes select a native composition and draw each amount range; patrol spawning consumes each native list member. No HCM gameplay Lua changed in this closure.

## Reproduction and provenance

Set `DARKTIDE_SOURCE=D:/Projects/game-data/source`, `DARKTIDE_TEST_RUNTIME=D:/Projects/dev-support/test-runtime`, and `DARKTIDE_HED_SOURCE=D:/Projects/dev-support/installed-mod-fixtures`, then run `tests/run.py` with the existing bundled Python. Git ownership allowances are process-scoped to the two exact repositories. No global Git settings, new installations, optional-mod updates or paid services are required.

Fresh bounded extraction confirms **70/70 installed modules** match that public source by the existing Lua-token lexer: all 59 breed tag definitions, enum/settings/role utilities, relevant pacing/horde/patrol consumers, and the native health-station method. Steam build `25606770`, executable FileVersion `1.3.802.934`; input database, executable and Oodle hashes remain unchanged. This supplements the prior accepted 14-module API/lifecycle comparison. The first supplemental decode attempt lacked its output directory and returned 1; the corrected clean capture succeeded and is the verified report. No lexer rules were weakened.

The parser also matches Lua evaluation of all **57 actual old 1.12.5 tag blocks**, including its 12 elite breeds. This checks old literal syntax; it does not claim the full current-source fixture suite runs against old game APIs.

Evidence: `validation/full-suite-all-before-fixture-20261003.txt`, `full-suite-all-after-fixture-20261003.txt`, `full-suite-default-closure-20261003.txt`, `suite-installed-source-70-20261003.json`, `legacy-breed-fixtures-20261003.json`, and `suite-fixture-provenance-20261003.json`. The runner now writes per-case status/environment and tested payload hashes to `build/checks/tests-result.json`; new candidate creation requires a passing complete report matching every source payload byte.

The historical `4.5.1-test.1` ZIP remains unchanged at SHA256 `94508d924a1de7ed3dec3e5e007503faaa06d6eae1f46d9e01748864fc84513f`. Its bundled warning describes the historical fail-fast checkpoint. A subsequent candidate can carry the coherent full-suite result.

Live game launch, DMF reload/unload, actual UI/settings/mission transitions, SoloPlay/Realms combinations and matched gameplay frame-time measurements remain unperformed. Offline Lua and UI fixtures do not establish FPS improvement. The accepted minion gate and its measurements are unchanged. Rank 80 and Fading Light III/IV remain a separate, unimplemented milestone.
