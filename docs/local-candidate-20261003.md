# Local candidate validation — 2026-10-03

## Current candidate 4.5.1-test.2

The full default `tests/run.py` suite passes all **37 scripts**, with no skipped cases or removed assertions. Fixture/source root causes and the complete before/after failure record are in [full-suite closure](full-suite-closure-20261003.md). The original compatibility repair and accepted minion gate are unchanged. Test closure commit: `e901f8fc4fc0e80a3bf9ee45f3c6dae971b36c18`.

ZIP: `build/local-candidates/4.5.1-test.2/HavocConditionManager-4.5.1-test.2.zip`; **603,883 bytes**, **323 payload files**, SHA256 **`72371695e2c77bf093dcc0db90c3101b4ae60457cd605b18fac0e885496770c6`**. All **122 Lua/mod files** compile and are byte-identical to the preserved test.1 ZIP. Exactly five payload files differ: version metadata, candidate changelog and the three localized README warnings. CRC, paths/case uniqueness, local imports, exact source equality and nested-archive checks pass.

The builder requires a passing complete suite report whose payload hashes match every packaged source byte. Re-run `tools/local_candidate.py --check` with the existing `DARKTIDE_TEST_RUNTIME` to validate this current candidate. Evidence: `validation/candidate-2-full-suite-20261003.txt`, `candidate-2-full-suite-result-20261003.json`, `local-candidate-2-package-20261003.json`, and `candidate-payload-comparison-20261003.json`.

Fresh installed-source correspondence passes **70/70 modules**, including every current breed tag definition and the additional fixture-consumed contracts; prior accepted API/lifecycle correspondence remains 14/14. Mocked/source tests cover the current 1.13.1 schema, old API/literal boundaries and actual existing HED 3.2.0 sources. Live SoloPlay/Realms gameplay, DMF reload/unload, actual UI/settings/mission transitions and matched gameplay frame-time measurements remain pending. Mocked timings do not establish FPS improvements.

The branch metadata identifies an unpublished Optional Files test candidate. No game/Studio sources were changed, and no deployment, push, publication, dependency installation or Havoc80 feature work occurred.

## Historical candidate 4.5.1-test.1

The record below describes the earlier fail-fast checkpoint at `a4c5eb7`. Its ZIP and separate validation manifest are preserved. Its source equality check requires that historical source; the current checker targets test.2.

Compatibility commit: `9a3d0de6e0513e3a039e12a740e6d8298bb08a20`. Independently accepted minion-gate commit: `a5f0c58da7ad077395435e1ca07029fdfaaa4006`. The candidate is `4.5.1-test.1`, using the repository's existing test-version convention; it is not a public release and has not been deployed.

ZIP: `build/local-candidates/4.5.1-test.1/HavocConditionManager-4.5.1-test.1.zip`; **603,352 bytes**, **323 payload files**, SHA256 **`94508d924a1de7ed3dec3e5e007503faaa06d6eae1f46d9e01748864fc84513f`**. All **122 Lua/mod files** compile from the ZIP; CRC, path/case uniqueness, byte-for-byte source equality, local imports, version and nested-archive checks pass. The candidate source's seven selected scripts pass, zero failed. Evidence: `validation/candidate-seven-checks-20261003.txt` and `validation/local-candidate-package-20261003.json`. Run `tools/local_candidate.py --check` with `DARKTIDE_TEST_RUNTIME` pointing to the approved isolated Lupa directory to revalidate the immutable ZIP against this source.

### Broader documented aggregate

README documents `./Test.ps1`, whose underlying aggregate is `tests/run.py`; `tests/README.md` also documents this direct entry point. Ran the default, unfiltered `tests/run.py` with existing bundled Python 3.12.14, approved isolated Lupa 2.6 and `DARKTIDE_SOURCE=D:/Projects/game-data/source` pinned to clean `7e662fc`. Git ownership exceptions were command/environment scoped; no global Git configuration changed.

The fail-fast runner completed six scripts successfully: syntax, current compatibility, replacement/loading, real Windows filesystem FFI, native minion lifecycle and minion stat gate. It then failed `native_template_tests.py`, Lua assertion line 27: **`Coarse control has no consumers: elite_density`**. Remaining aggregate scripts were not run. No skip or runner redefinition was used, and no full-suite passing claim is made. See `validation/full-suite-20261003.txt`.

The same test failed with exactly the same assertion against the original `247fe0352ed86f5b10fc8fc4ba0589ace0b024cf` runtime source and the same current native source/runtime. The baseline copy restores all four modified production files from locally present original Git blobs; other runtime files and the test/harness/load-event helper are unchanged from that revision. The current filesystem-isolation helper is supplied to both runs only to confine I/O safely. See `validation/full-suite-baseline-247fe03.txt`. This establishes a pre-existing aggregate failure under 1.13.1, not a new gate/repair regression; it does not by itself establish a live gameplay defect or whether the coarse-control assertion should be revised.

### Candidate packaging and limits

`tools/local_candidate.py` creates/checks only a local candidate under ignored `build/local-candidates`, with an immutable ZIP and a separate validation manifest. It preserves source payload bytes and reuses the existing nested-archive guard and extension rules. It does not invoke or bypass the public release builder; that builder requires a passing default aggregate and publishing configuration not materialized in this sparse checkout.

The ZIP has only `HavocConditionManager/` from `src/HavocConditionManager`, including its descriptor, scripts, DIY content, metadata and bundled documentation. No repository tests/tools/evidence, game sources, native executables/DLLs, nested archives or optional collection animation patches are included. Validation checks ZIP CRC, paths/case uniqueness, byte-for-byte source equality, version, local imports and compilation of every packaged Lua/mod file using the approved runtime. Full-runner status and unperformed gameplay validation are explicitly recorded in the candidate changelog and separate validation manifest. Durable evidence copies under `docs/validation` normalize line endings to LF; original captured hash records remain at their recorded paths.

Seven focused regression scripts and 14/14 selected installed native-module comparisons are the accepted scope. Actual gameplay, live DMF reload/unload, settings/UI/mission transitions, optional-mod combinations and matched frame-time measurements remain outstanding. Mocked callback timing is not an FPS claim. No push, publication, game launch or deployment occurred.
