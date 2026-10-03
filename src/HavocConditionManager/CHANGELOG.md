# Local candidate 4.6.0-test.1 — 2026-10-03

Unpublished local feature candidate. Custom Havoc ranks1–50 and Emperor's Fading Light III/IV have bounded offline acceptance; SoloPlay mission data retains native rank40/II identity with separate HCM metadata. III/IV extend only captain travel, monster-slot chance/cooldown and horde timer pacing from native I/II anchors. Native I/II, eligibility, concurrency and remaining mechanics are preserved.

The40-case offline suite covers native initialization/consumers, mission/settings/reload ownership, actual HED preset/mode/capture/rollback and UI callbacks. Shorter timers raise potential workload; no FPS claim is made. Live UI, persistence, DMF reload, gameplay and frame-time checks remain unperformed. This candidate includes runtime scripts, built-in DIY, loader/metadata and attribution; authoring docs/examples and validation fixtures stay outside the ZIP.

# Local candidate 4.5.1-test.2 — 2026-10-03

This ZIP is an unpublished local test candidate. It has not been deployed or validated in a running game.

The full default offline suite passes: all 37 scripts, with no omitted assertions or skipped failures. Current game-source fixture parsing, native special-slot/heat contracts, relocated medical package tests, actual optional HED UI sources and tracked sparse release fixtures are corrected. Fresh extraction confirms 70/70 relevant installed native modules match the pinned 1.13.1 source, including all 59 breed tag definitions, in addition to the previously accepted 14 API/lifecycle modules. The older literal-tag parser is checked against 57 actual 1.12.5 definitions.

Compatibility fixes and the independently accepted minion stat gate are unchanged from candidate 4.5.1-test.1. Its ZIP/hash remains a historical checkpoint. This candidate updates only version and validation documentation in the runtime payload.

Live DMF reload/unload, UI/settings/mission transitions, SoloPlay/Realms combinations and matched gameplay frame-time measurements remain pending. Mocked callback timing does not establish an FPS improvement. Rank 80 and Fading Light III/IV are separate, unimplemented work.

# Local candidate 4.5.1-test.1 — 2026-10-03

This ZIP is a local test candidate. It has not been published or validated in a running game.

- Adapt the difficulty picker to the current native danger-level table while retaining the older layout.
- Forward the forced sub-faction and trailing arguments through native roamer construction.
- Prepare pacing/heat replacements before native derived-state updates and preserve deferred monster processing.
- Respect mutator loading readiness, repeated-load ownership and native activation order.
- Adapt DIY minion update registration to the current unit/reason API, preserving independent pauses and native buff ownership.
- Adapt DIY ability cooldown recovery to native ability resources while retaining legacy and grenade semantics.
- Skip player-only client-effect probes in concrete minion stat callbacks. Player effects, overlays and cache invalidation retain their tested behavior. Mocked callback measurements do not establish an FPS improvement.

Seven selected regression scripts pass and the 14 selected native API/lifecycle modules match the installed build by Lua tokens. The documented full test runner stops at `native_template_tests.py`: `Coarse control has no consumers: elite_density`. The original 4.5.0 source reproduces that assertion with the same current native source/runtime; the remaining full-runner scripts were not executed after its fail-fast stop. This candidate therefore does not have full-suite acceptance.

Actual gameplay, live DMF reload/unload, UI, settings/mission transitions, optional-mod combinations and frame-time behavior remain unvalidated. No installed game files are included or changed.
