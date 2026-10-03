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
