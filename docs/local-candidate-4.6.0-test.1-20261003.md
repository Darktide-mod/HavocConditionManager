# Local candidate 4.6.0-test.1

This unpublished candidate combines the accepted game-update compatibility/performance fixes, custom Havoc ranks 1-50, and custom Emperor's Fading Light III/IV. The rank50 checkpoint is `17851628cc9ae8de03ccf4a13c06222fe61f38f2`; the independently accepted EFL implementation is `0dc39a50d61a67be3af1247a44a9b1092786fa75`. The final preparation changes version metadata, runtime packaging policy and evidence documentation; it adds no gameplay behavior beyond those accepted checkpoints.

## Deliverable and package policy

Archive: `build/local-candidates/4.6.0-test.1/HavocConditionManager-4.6.0-test.1.zip`.

SHA256: `4e5e3aeb58763a03137a149122c954a7075a06a3c7bf1e6d29068c0aba07d6b4`. Size: 246,138 bytes. It contains 79 files, including all runtime scripts, bundled DIY manifests/packages/assets, the `.mod` loader, `info.json` and third-party attribution. The 249 excluded authoring files are guides/package examples and the source changelog. No game-source extraction, tests, test evidence, development tools or nested archive is included. All 74 Lua/`.mod` files compile with the approved LuaJIT runtime; CRC, exact source bytes, path layout and literal local imports pass.

A separate read-only ZIP review independently confirmed the archive hash/size, CRC, exact runtime allowlist and current-source bytes, all 64 literal local imports and three loader targets, and built-in DIY index/manifest/definition/Lua completeness. It found no blocker and did not rebuild the archive or rerun the suite.

The positive packaging allowlist has regression coverage in the existing suite-evidence check. The fresh complete gate still hashes all 328 source files and all 66 test/package-tool inputs before and after the aggregate, rather than weakening its source comparison to only the 79 archived files. Missing required roots, extra authoring files or stale/partial evidence are refused. Older 4.5.1-test.1/test.2 archives remain byte-identical; the [closure record](validation/4.6.0-test.1-evidence-closure-20261003.json) preserves their original hashes.

## Source provenance correction

The nonblocking P3 finding in the [independent review](../../HavocConditionManager-review/efl-four-tiers-20261003/independent-final-review.md) is corrected in [the EFL document](custom-efl-four-tiers.md). The 15-module rank50 report covers none of the nine EFL files. Three pacing consumers instead use the earlier verified suite-source report; PacingManager uses the earlier installed-source extraction. The reviewer rechecked those four hash triples.

The remaining five definition/consumer modules were then extracted in a bounded operation using the previously pinned limn/decompiler and token lexer, with one extraction worker and no installation. All five match public-source tokens at `7e662fcda16219d775b84af50322be2e9cd9d62e`. Their bytecode, decoded/public hashes, commands, tool pins and unchanged executable/database/Oodle inputs are recorded in [the five-module report](validation/efl-source5-20261003.json). This report extends installed correspondence only to those exact five modules. Darktide executable PE `1.3.802.934` / Steam build `25606770` and source version 1.13.1 are separate identifiers; DMF's exact runtime version remains unconfirmed.

## Validation and limits

The final full aggregate passes 40/40 with ordered integer-zero exits and stable pre/post input hashes. Its [exact result](validation/4.6.0-test.1-full-suite-result-20261003.json) has SHA256 `24e66a62362af185795e53139dd782972f2e056868aa09f3ee2e805b504eb31d`. See the [per-case log](validation/4.6.0-test.1-full-suite-20261003.txt), [package validation](validation/4.6.0-test.1-package-validation-20261003.json), and [EFL synthetic workload](validation/4.6.0-test.1-workload-20261003.json).

Coverage includes pinned native consumers, rank/tier combinations, settings changes, mission transitions, disable/reload/unload, optional-mod absence/late appearance, HED transactions and owned-state cleanup. Native I/II behavior and the complete II bundle remain preserved within existing independent settings semantics. Custom III/IV increase scheduling pressure; the deterministic workload measures candidate counts and cached preparation calls, not gameplay FPS. The earlier callback microbenchmark likewise supports only its measured Lua workload, not a frame-rate claim.

Live UI/rendering, real disk persistence, DMF reload, mission gameplay and frame-time measurements remain unperformed. The parent's UI investigation positively found the desktop locked at 21:43 UTC; user unlock is required before those checks. No game launch, installed-mod deployment, public match/progression action, push or publication was performed. No new dependency was installed. The radar project and GPU were untouched.
