# NuvioDV Playback Details Specification

Authorization: `already_authorized` by the user on 2026-09-12.

## Requirements

- R1: Keep the existing top-left title, episode, stream, and provider metadata unchanged.
- R2: Add one bottom metadata row containing technical facts for the video that the active player actually loaded.
- R3: The row must include available resolution, video codec, dynamic range, and frame rate, in that order, separated by bullets.
- R4: Use concise labels such as `4K`, `HEVC`, `DV`, and `23.976 FPS`; omit unavailable facts and hide the row when every fact is unavailable.
- R5: Populate the facts for both Android playback engines without changing playback selection or rendering behavior.
- R6: Add a persisted, syncable `Show playback details` toggle under General > Playback > Decoder settings, enabled by default, which controls the technical row.
- R7: Publish the verified implementation as the next normal GitHub release, not a prerelease.

## Acceptance criteria

- AC1: Focused common tests verify formatting, ordering, normalization, omission, and row hiding.
- AC2: Android compilation verifies both ExoPlayer and libmpv metadata extraction integrate with the shared player UI.
- AC3: The existing header renders the technical row beneath its current source/provider row.
- AC4: The completed and verified change is committed to `cmp-rewrite`.
- AC5: The settings toggle is present in Decoder settings, defaults on, persists, syncs, and hides the row when off.
- AC6: The public normal release and APK independently verify the intended version, package, signer, ARM64 libmpv/libdovi payload, and checksum.

## Stages and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Playback metadata model and formatting | COMPLETE | R2-R4 | Focused formatter tests pass |
| Android engine extraction, header integration, and settings toggle | COMPLETE | R1, R2, R5, R6 | Focused persistence/sync test and complete debug APK build pass |
| Final reconciliation, commit, and release | COMPLETE | R1-R7 | Feature commit `7066fe3e`; corrected release commit `61e4eb15`; workflow run `34690741856`; normal release `v0.4.17-nuviodv.5`; independently verified public APK package, version, signer, ARM64 payload, libdovi symbols, and SHA-256 |

Blockers: none.

Tracked deferrals: none.

## Final release evidence

- GitHub release: `v0.4.17-nuviodv.5` (`isPrerelease=false`), built from `61e4eb15f69b615b92f09aabd36337c6bb2fce84`.
- Public APK: `NuvioDV-0.4.17-nuviodv.5-arm64-v8a.apk`.
- Package identity: `com.darkaxt.nuviodv`, versionCode `12207`, versionName `0.4.17-nuviodv.5`, label `NuvioDV`.
- APK SHA-256: `13D53F231353AD1BECAD77A6FA2EE69B76338BF3E15DF3C871BEBF83B83A1231`.
- Signing certificate SHA-256: `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`.
- Native verification: APK advertises only `arm64-v8a`; its `libmpv.so` exports `dovi_parse_rpu` and `dovi_parse_rpu_bin_file`.
