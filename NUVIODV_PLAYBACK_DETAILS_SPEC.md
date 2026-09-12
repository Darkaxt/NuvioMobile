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
| Final reconciliation, commit, and release | ACTIVE | R1-R7 | Fresh tests, Android build, and independent public artifact verification |

Blockers: none.

Tracked deferrals: none.
