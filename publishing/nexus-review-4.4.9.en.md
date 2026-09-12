# HavocConditionManager 4.4.9 — information for manual review

Mod page: https://www.nexusmods.com/warhammer40kdarktide/mods/1267

File: HavocConditionManager-4.4.9.zip, uploaded under version 4.4.9; 6,711,372 bytes.

SHA-256: `4957498ea6edc2e13828356c308cc6235f94301a39f1395b277fadaaa2f9d89b`

The file page displays the generic automated-quarantine notice. We do not have the specific rule, detection name or affected member path. Please identify the trigger and review the attached installer sources and original upload.

## Archive inspection

The ZIP contains 397 files under a single HavocConditionManager directory. Every member passes the ZIP CRC check. Each extracted member was inspected with 7-Zip 26.00, Windows tar/libarchive and file/libmagic. None was recognized as an inner archive by the archive tools. The 54 .patch_996 files are game animation resource containers; neither archive tool opens them as an archive. The embedded Lua package templates contain plain text, not compressed data.

A Microsoft Defender custom scan of the original ZIP, with remediation disabled, completed with exit code 0 and reported no threats. This is one local engine result, not a VirusTotal or Nexus clearance.

## Installer sources and behavior

The upload contains no precompiled EXE or DLL. It includes two CMD launchers and one PowerShell installer:

- `HavocConditionManager/Install-native-melee.cmd`
- `HavocConditionManager/Uninstall-native-melee.cmd`
- `HavocConditionManager/native-melee/Install.ps1`
- `HavocConditionManager/native-melee/manifest.json`
- `HavocConditionManager/docs/Native-melee-installation.md`

The CMD files run PowerShell with a process-local execution-policy argument. The PowerShell script includes its complete C# source in an Add-Type block. That code parses the game's local resource-registration database and preserves unrelated records. No compiled installer assembly is distributed.

With the game closed, the installer verifies the executable and source-resource hashes, installs 54 native animation resource patches, updates six files in the local Frenzied assault package, and retains backups and a transaction ledger. It rejects path escapes, linked target paths, changed installed files and unknown conflicts. It supports failed-upgrade rollback and removal. It hashes the game executable but does not patch its executable code.

The installer performs no network downloads, scheduled-task or service registration, startup registration, or privilege-elevation request.

## Reproduction and source access

The full project is in https://github.com/Darktide-mod/HavocConditionManager at commit `4a2f275612908ea15272cfca06032dffb3506f7f`. It is a private organization repository, so the link alone will not give outside reviewers access. The five source/document files listed above can be supplied directly with the review request; they are already present, unencrypted, in the quarantined upload.

The inline C# is compiled by Windows PowerShell's built-in Add-Type command when the installer runs. There is no separate native DLL build or opaque binary installer dependency. Use `Install.ps1 -Mode Check -GameDirectory <game directory>` to perform preflight validation without installation. Use the synthetic regression in `tests/native_melee_installer_tests.py` to exercise install, removal, verified upgrade, rollback and conflict handling in temporary fake game directories.

The project contains the prebuilt animation payloads and their SHA-256 manifest. Its ordinary release process packages those verified payloads; it does not regenerate game assets or compile a hidden executable. To inspect the upload independently, extract the ZIP and run an archive-listing tool against its members. The mod's Lua code can be read directly under `HavocConditionManager/scripts/mods/HavocConditionManager`.

The original quarantined upload is retained. No file has been renamed or encoded to hide executable content, and no Nexus review outcome is claimed here.
