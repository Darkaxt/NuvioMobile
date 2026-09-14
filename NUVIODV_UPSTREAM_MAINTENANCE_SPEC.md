# NuvioDV Upstream Maintenance Specification

Authorization: `already_authorized` by the user on 2026-09-12.

## Requirements

- M1: A GitHub Actions workflow must check `NuvioMedia/NuvioMobile` branch `cmp-rewrite` daily.
- M2: When no upstream commit is missing from `Darkaxt/NuvioMobile:cmp-rewrite`, the workflow must not create a commit, push, or release.
- M3: When upstream commits are missing, merge their history into the fork without discarding NuvioDV changes. The workflow may automatically preserve the fork's `iosApp/Configuration/Version.xcconfig` during a conflict limited to that file; any other merge conflict must fail closed for manual repair.
- M4: Each synchronized release must retain the exact current upstream semantic version as its base and advance the Android version code. If upstream remains on the same version, increment only the `-nuviodv.#` fork counter; if upstream advances its version, adopt it and reset the fork counter to `1`; fail closed if upstream appears older than the fork base.
- M5: Before pushing, verify the NuvioDV package identity, app label, local patched libmpv dependency, authenticated-release test, and a full Android debug APK build. A failed invariant or build must prevent the push and release.
- M6: After pushing the verified sync commit, dispatch the authenticated NuvioDV release workflow with that exact commit as an explicit checkout input. Every published NuvioDV build must be a normal GitHub release; branch-ref propagation must not be allowed to publish an older commit.
- M7: A recurring Codex check must run every three days. It must inspect upstream divergence and daily-workflow/release results; if GitHub automation failed or left commits unsynchronized, it is authorized to diagnose, make the minimal fork-preserving repair, verify, commit, push, and trigger the release itself.
- M8: The three-day check must also inspect new or newly updated open upstream issues for playback problems relevant to NuvioDV, libmpv, Dolby Vision, libplacebo/pink output, hardware decoding, renderer/color-format behavior, subtitles/audio interaction, or long-playback pipeline failure.
- M9: Issue monitoring must not comment on upstream issues or automatically broaden the fork. It reports only evidence-backed candidates worth considering and stays quiet when neither maintenance nor issue triage produces an actionable change.
- M10: Public release history must contain only tags whose left-side version matches the upstream release represented by their source commit. Superseded misnumbered releases and tags must be removed after their audit metadata is recorded.
- M11: The canonical retained releases are `v0.4.17-nuviodv.5`, `v0.4.18-nuviodv.1`, `v0.4.18-nuviodv.2`, and `v0.4.19-nuviodv.1`; all four must be normal releases, and `v0.4.19-nuviodv.1` must remain the latest release.

## Acceptance criteria

- MC1: Version-advance tests prove same-base fork-counter increments, newer-upstream resets, older-upstream rejection, and a higher Android version code.
- MC2: The daily workflow parses, has write permissions needed for source sync and release dispatch, and contains fail-closed merge/build behavior.
- MC3: A manual workflow dispatch consumes the currently pending upstream commits, preserves fork invariants, pushes the verified merge, and dispatches a successful authenticated normal release.
- MC4: A three-day Codex heartbeat is active with the authorized remediation and playback-issue scope.
- MC5: Repository changes and maintenance evidence are committed and pushed to `cmp-rewrite`.
- MC6: Release-policy tests reject prerelease inputs/flags and prove the daily sync dispatches the normal release workflow.
- MC7: A fresh GitHub API audit proves only the four canonical releases/tags remain, all are normal releases, and the latest release is `v0.4.19-nuviodv.1`.

## Stage and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Daily verified upstream sync and release | COMPLETE | M1-M6 | Runs 34665705660 and 34666617695 consumed the initial pending commits; source-SHA input fixes branch-ref propagation race; run 34667333366 verified the unchanged-upstream no-op path; version contract corrected in `61e4eb15`; on 2026-09-13 run 34723027169 failed closed on four overlapping player-settings files plus the expected version conflict, after which merge `b62001d` retained both upstream settings and NuvioDV playback details and release run 34723777285 published verified prerelease `v0.4.18-nuviodv.1`; on 2026-09-14 sync run 34786755533 consumed seven upstream commits without conflicts and release run 34787071223 published verified prerelease `v0.4.19-nuviodv.1` from exact source `4ea1125` |
| Three-day Codex maintenance and issue triage | COMPLETE | M7-M9 | Active heartbeat `maintain-nuviodv-upstream-fork` runs every three days with authorized remediation, quiet no-change behavior, and issue-delta triage; baseline reviewed all 343 open issues and records #1730 as high relevance while #1675/#1723 remain low confidence |
| Public release-lineage repair | ACTIVE | M6, M10-M11 | MC6 test is red against the former prerelease workflow; exact keep/delete manifest recorded from GitHub release/tag/source/upstream-base evidence |
| Final reconciliation | NOT STARTED | M1-M11 | Requires MC1-MC7 with blockers and tracked deferrals equal zero |

Blockers: public release cleanup and normal-release workflow conversion are not yet complete.

Tracked deferrals: none.

## 2026-09-13 sync incident

- Upstream advanced by 33 commits after the preceding scheduled run and released Nuvio `0.4.18`.
- The immediate manual dispatch failed closed before any push or release because upstream's loading-status and pause-overlay settings overlapped NuvioDV's playback-details setting in four repository/storage files; `Version.xcconfig` was the fifth conflict.
- Manual resolution retained all three settings across the shared repository plus Android and iOS storage/sync paths.
- Focused version/workflow contracts and the three affected Android player-settings tests passed; the integrated full debug APK built successfully as `0.4.18-nuviodv.1` with versionCode `12208`.
- The earlier `v0.4.18-nuviodv.1` release and tag, created from commit `b566cf8` under the superseded version algorithm, blocked the canonical upstream-`0.4.18` tag. Its published metadata and APK checksum `DAFABBED4D76FC39FA0D72860BD1D8C7A37C2FA187416943E5A7643CB43A771A` were recorded before deleting that obsolete release/tag; the source commit remains in repository history.
- Release run `34723777285` succeeded against exact source commit `b62001dbce2d8f132dafca3b86680de87bbdf9f5` and published prerelease `v0.4.18-nuviodv.1`.
- Independent download verification confirmed APK SHA-256 `8018D2F9BBB44BE4D527B09897186A86F9E1AB12A16F56F3FCA4F2E5ED839DBF`, package `com.darkaxt.nuviodv`, label `NuvioDV`, versionCode `12208`, versionName `0.4.18-nuviodv.1`, ARM64-only native code, APK Signature Scheme v2, signer certificate SHA-256 `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`, and exported `dovi_parse_rpu` plus `dovi_parse_rpu_bin_file` symbols in `libmpv.so`.

## 2026-09-14 sync

- Upstream advanced by seven commits and released Nuvio `0.4.19`; sync run `34786755533` merged the history without conflicts, passed fork invariants and the integrated Android build/APK verification, then pushed exact release source `4ea112503236b6b7b4d16dfcbac4a6ecd6db667c` as `0.4.19-nuviodv.1` with versionCode `12210`.
- The first release dispatch failed closed because obsolete prerelease/tag `v0.4.19-nuviodv.1`, created from commit `3dfb5cb` while its upstream merge parent was still Nuvio `0.4.17`, occupied the corrected canonical tag. Its APK checksum `58FFEA699A7806D142EA62E663668BEE0AAC3CA365006FD36FF5356FE645CF7D`, publication time, two-download count, and target commit were recorded before deleting that obsolete release/tag; its source commit remains in history.
- Release run `34787071223` succeeded against exact source commit `4ea112503236b6b7b4d16dfcbac4a6ecd6db667c` and published prerelease `v0.4.19-nuviodv.1`.
- Independent download verification confirmed APK SHA-256 `E0D042B78CFDF1C7F7EDC7BFE395EB0B1E8F9E3CED345D0CCE391D0F24D3E4A6`, package `com.darkaxt.nuviodv`, label `NuvioDV`, versionCode `12210`, versionName `0.4.19-nuviodv.1`, ARM64-only native code, APK Signature Scheme v2, signer certificate SHA-256 `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`, and exported `dovi_parse_rpu` plus `dovi_parse_rpu_bin_file` symbols in `libmpv.so`.
