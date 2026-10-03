# Rank50 optional HED API appearance — P2 closure

Baseline reviewed: `47604405b42b8a7c195a205460eca1d24db0e4dc`. Narrow implementation/regression commit: `6636146`, branch `feature/custom-havoc-rank50`. The [independent checkpoint review](../../HavocConditionManager-review/rank50-checkpoint-independent-review-20261003.md) found that the bridge reported successful reinstallation while a newly published HED HCM-mode capture method remained unwrapped. Its direct document capture therefore retained native40 and omitted requested50 metadata.

The bridge previously recorded only methods it actually wrapped. It now records the original identity of every supported slot, including absent/non-function values. Reusing an installation requires each current slot to equal its owned wrapper or its recorded original value. A function appearing or being replaced on the same owner/presets/codec tables therefore triggers owner-safe retirement and reinstallation. Uninstall restores a slot only when an actual HCM wrapper still occupies it. A newly published untouched method or third-party replacement is preserved; retired captured HCM wrappers remain inactive.

Only `custom_havoc_rank_presets.lua` and `tests/custom_havoc_rank_tests.py` changed in the fix commit. The ordinary curves, native identity, settings, native source fixtures and all existing37 test scripts were unchanged. EFL III/IV remain unimplemented.

The saved independent reproduction was replayed with the bridge loaded from frozen4760440, confirming its original failure and explicit-uninstall control. The same saved setup with the current bridge confirms automatic late capture wrapping, native40/requested50 metadata, repeated-install identity and original-function restoration. Its mock Director validator discards mission fields on normalization, so this replay checks the owned native-rank record/SoloPlay rank; the full regression uses the actual HED validator and also asserts document mission rank40. The reviewer reproduction itself was not edited.

New assertions use the actual HED HCM capture branch and cover:

- Each of the five optional methods appearing from nil and false on unchanged objects/tables.
- All six supported methods replaced in place, including codec validation.
- Five repeated installation calls per appearance/replacement retaining every method identity.
- A method published after an absent-slot installation but before uninstall remaining untouched.
- Required codec validation absence/refusal, followed by publication and successful installation.
- A third party holding an old HCM wrapper: reinstallation preserves its call chain, injects metadata exactly once, and uninstall preserves the third-party function.

Focused rank/evidence/syntax checks pass (3/3). The complete canonical suite passes39/39 with one ordered integer-zero exit per required case. Current-source evidence gate passes without building an archive:326 source hashes and65 test/tool hashes match before/after/current. The full-result SHA256 is `45fdf75680846e0f2cbf66977a932991e593fc7aa5bacdbaa3d247c0e623d434`.

Evidence:

- [Frozen/current reproduction replay](validation/rank50-p2-repro-closure-20261003.txt)
- [Focused results](validation/rank50-p2-focused-result-20261003.json), [focused log](validation/rank50-p2-focused-20261003.txt)
- [Complete39-case results](validation/rank50-p2-full-suite-result-20261003.json), [per-case log](validation/rank50-p2-full-suite-20261003.txt)
- [Current-source gate and preserved archive fingerprints](validation/rank50-p2-evidence-gate-20261003.json)

The original4760440 milestone evidence and independently reviewed artifacts remain unchanged. Test.1/test.2 ZIP fingerprints remain unchanged. Sandbox command execution initially disconnected; the existing authorized executor channel successfully ran these local checks. No new dependency, global Git configuration, installed mod/settings, game launch, packaging, release or push occurred.

This closes the writer's bounded P2 implementation/test work and returns the new frozen commit for independent review. Real disk persistence, DMF reload, gameplay/frame-time and multiplayer remain unperformed; no FPS claim is made. External native/HED fixtures are outside the suite's pre/post hash maps and retain their separate provenance.
