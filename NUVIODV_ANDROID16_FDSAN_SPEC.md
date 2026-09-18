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
| Device and release verification | BLOCKED | FDSAN-2, FDSAN-4 | Release and install verification pass; direct-playback log inspection is blocked by the tablet's secure keyguard |

Release evidence:

- Commit `5de24225c9af0df412ab9ba2b59cd4c06bbefce7` is pushed to `cmp-rewrite`.
- Workflow run `35367593482` built, verified, and published the signed ARM64 APK.
- Release `v0.4.23-nuviodv.6` targets the exact verified commit.
- The published APK reports package `com.darkaxt.nuviodv`, version `0.4.23-nuviodv.6`, version code `12219`, and ARM64-only native libraries.
- The published APK contains the RPDB logo and libmpv/libdovi symbols; its SHA-256 matches the GitHub release digest.
- The signed APK installs successfully on Samsung tablet `R52W60CFTRL` and the installed package reports version code `12219`.

Blocker:

- AC3 is externally blocked because `R52W60CFTRL` is secured by an active keyguard with input restricted. The condition resolves when the tablet is unlocked, after which direct playback can be launched and logcat checked for `ytdl_hook`, `Subprocess failed`, and `fdsan`.

Tracked deferrals: none.
