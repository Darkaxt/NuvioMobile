# NuvioDV Android 16 libmpv FDSAN Specification

Authorization: `already_authorized` by the user on 2026-09-18.

## Evidence

- Two Samsung Android 16 crashes terminated `com.darkaxt.nuviodv` with native `SIGABRT` after `fdsan` detected invalid file-descriptor ownership.
- The second crash occurred while libmpv's `ytdl_hook` attempted an unavailable subprocess and reported `Subprocess failed: init`.
- Nuvio supplies resolved direct media URLs to libmpv and the bundled AAR does not provide a working yt-dlp executable, so the hook cannot successfully resolve a source.

## Requirements

- FDSAN-1: Disable libmpv's built-in `ytdl` hook before native initialization.
- FDSAN-2: Preserve direct HTTP, HTTPS, HLS, local-file, hardware-decoding, renderer, subtitle, and libdovi behavior.
- FDSAN-3: Do not suppress Android `fdsan`, weaken process-wide diagnostics, or alter unrelated player lifecycle behavior.
- FDSAN-4: Include the fix in the same `0.4.23-nuviodv.6` release as the branded RPDB integration icon.

## Acceptance Criteria

- AC1: A focused host test proves the Android libmpv initialization policy sets `ytdl=no`.
- AC2: The Android full-debug APK builds and packages the existing ARM64 libmpv/libdovi payload.
- AC3: Device-side launch logs for direct playback do not contain a `ytdl_hook` subprocess attempt.
- AC4: The verified commit is pushed to `cmp-rewrite` and the signed release workflow publishes `0.4.23-nuviodv.6` / `12219`.

## Stages

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Reproduce and isolate | COMPLETE | FDSAN-1-FDSAN-3 | ADB exit history, crash tombstones, and timestamped libmpv logs identify the unsupported subprocess path |
| Disable unsupported subprocess resolution | COMPLETE | FDSAN-1-FDSAN-3 | Focused red/green host test, all Android player host tests, and full-debug APK build pass |
| Device and release verification | ACTIVE | FDSAN-2, FDSAN-4 | Direct-playback log inspection, release workflow, and independent APK inspection |

Blockers: none.

Tracked deferrals: none.
