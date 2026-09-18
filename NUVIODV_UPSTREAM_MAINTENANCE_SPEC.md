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
- M11: The four releases retained by the 2026-09-14 lineage repair remain valid historical releases. Later verified sync releases may extend that set; every current release must be normal and the latest release must be the newest verified NuvioDV version.
- M12: The NuvioDV in-app updater must query `Darkaxt/NuvioMobile` normal releases, not the upstream `NuvioMedia/NuvioMobile` feed.
- M13: Upstream synchronization must preserve the fork's `.github/workflows` tree so the default GitHub Actions token never attempts a forbidden workflow-file push; upstream application history and all non-workflow files remain mergeable.

## Acceptance criteria

- MC1: Version-advance tests prove same-base fork-counter increments, newer-upstream resets, older-upstream rejection, and a higher Android version code.
- MC2: The daily workflow parses, has write permissions needed for source sync and release dispatch, and contains fail-closed merge/build behavior.
- MC3: A manual workflow dispatch consumes the currently pending upstream commits, preserves fork invariants, pushes the verified merge, and dispatches a successful authenticated normal release.
- MC4: A three-day Codex heartbeat is active with the authorized remediation and playback-issue scope.
- MC5: Repository changes and maintenance evidence are committed and pushed to `cmp-rewrite`.
- MC6: Release-policy tests reject prerelease inputs/flags and prove the daily sync dispatches the normal release workflow.
- MC7: A fresh GitHub API audit proves every retained release is normal and the latest endpoint resolves to the newest verified NuvioDV release.
- MC8: A regression contract fails against the upstream updater owner and passes only when the in-app release feed owner is `Darkaxt`.
- MC9: A regression contract proves upstream workflow-file changes are restored to the pre-merge fork tree before commit/push, while a real pending-upstream sync reaches zero commits behind and publishes the exact verified normal release.

## Stage and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Daily verified upstream sync and release | COMPLETE | M1-M6 | Runs 34665705660 and 34666617695 consumed the initial pending commits; source-SHA input fixes branch-ref propagation race; run 34667333366 verified the unchanged-upstream no-op path; version contract corrected in `61e4eb15`; on 2026-09-13 run 34723027169 failed closed on four overlapping player-settings files plus the expected version conflict, after which merge `b62001d` retained both upstream settings and NuvioDV playback details and release run 34723777285 published verified prerelease `v0.4.18-nuviodv.1`; on 2026-09-14 sync run 34786755533 consumed seven upstream commits without conflicts and release run 34787071223 published verified prerelease `v0.4.19-nuviodv.1` from exact source `4ea1125` |
| Three-day Codex maintenance and issue triage | COMPLETE | M7-M9 | Active heartbeat `maintain-nuviodv-upstream-fork` runs every three days with authorized remediation, quiet no-change behavior, and issue-delta triage; baseline reviewed all 343 open issues and records #1730 as high relevance while #1675/#1723 remain low confidence |
| Public release-lineage repair | COMPLETE | M6, M10-M11 | Commit `3f063f84` removed the prerelease input/flag paths and made normal releases the enforced workflow contract; invalid historical releases/tags were deleted after audit, and subsequent releases through `v0.4.23-nuviodv.1` are normal and preserve upstream-aligned left-side versions |
| Fork updater and workflow-permission repair | COMPLETE | M12-M13 | Commit `79a4adf1` points the regression contract and updater at the fork and preserves the fork workflow tree; upstream refactored the updater during the pending batch, so merge `79a32bc0` retained that refactor while routing `AppUpdaterRepository` to `Darkaxt/NuvioMobile`; local full-debug build passed, release run 35336010585 published the exact normal release, and no-update sync run 35336838855 passed |
| Final reconciliation | COMPLETE | M1-M13 | MC1-MC9 satisfied; fork is zero commits behind upstream, latest normal release and APK were independently verified, workflows and heartbeat remain active, blockers and tracked deferrals equal zero |

Blockers: none.

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

## 2026-09-14 public release-lineage repair

- Root cause: automated sync releases were explicitly configured as prereleases, while four earlier builds used invented left-side versions that did not match their actual upstream base. Update clients consequently saw installed `0.4.21-nuviodv.1` as newer than canonical `0.4.19-nuviodv.1` even though the latter had the higher Android versionCode.
- Commit `3f063f84` removed the prerelease workflow input and `--prerelease` publication branch. Daily syncs now dispatch only normal releases, matching the upstream project's delivery model and providing one monotonic public feed.
- The active three-day `maintain-nuviodv-upstream-fork` automation was updated to inspect and dispatch the normal-release workflow and to reject draft/prerelease publication.
- Deleted invalid release/tag `v0.4.17-nuviodv.1`: source `2a0c0aa`, actual upstream base `0.4.16`, APK SHA-256 `FD26E22A2BBE3A27D8B835FAEBD0B83C03B3049D58E256EE954257E9710423A0`, six downloads.
- Deleted invalid release/tag `v0.4.17-nuviodv.2`: source `11a3a98`, actual upstream base `0.4.16`, APK SHA-256 `9FA5031A5ABB56B6D91C9DF0B5FBFDDB8532DE294683D94BA9CD35FC5CCF4715`, four downloads.
- Deleted invalid release/tag `v0.4.20-nuviodv.1`: tag source `ddecc19`, actual upstream base `0.4.17`, APK SHA-256 `F30C8D29E4EC2AF851B354BFE633F05374A47D25FB0D32ED96CEC3EA798810EF`, one download.
- Deleted invalid release/tag `v0.4.21-nuviodv.1`: source `7066fe3`, actual upstream base `0.4.17`, APK SHA-256 `7DC5E4D584CDC45DD18603084ECAB7F043BB7AD09321C2C7009903EBE409240D`, four downloads.
- Retained `v0.4.17-nuviodv.5`, `v0.4.18-nuviodv.1`, `v0.4.18-nuviodv.2`, and `v0.4.19-nuviodv.1` because each tag resolves to a source whose upstream base matches its left-side version. All four are normal releases; `v0.4.19-nuviodv.1` is explicitly Latest. No retained artifact required rebuilding.

## 2026-09-18 updater and synchronization repair

- The in-app updater still queried `NuvioMedia/NuvioMobile`; upstream then refactored updater selection into `AppUpdaterRepository`, so merge `79a32bc0` retained the new stable/beta behavior and changed its GitHub endpoint to `Darkaxt/NuvioMobile`.
- Scheduled sync runs `35205432333` and `35327470164` had integrated and built upstream successfully but failed at push because upstream modified stock workflow files and GitHub's default Actions token cannot update workflow files. Commit `79a4adf1` makes future merges restore the fork's pre-merge `.github/workflows` tree before push.
- The first repaired live dispatch, run `35335125861`, failed closed on the updater refactor conflict plus the expected version conflict. Manual merge `79a32bc0` preserved upstream application changes, the fork updater endpoint, and fork workflows; the full debug APK then built successfully as `0.4.23-nuviodv.1` with versionCode `12214`.
- Release run `35336010585` published normal release `v0.4.23-nuviodv.1` from exact source `79a32bc00a26b19880681f3c325964689398b407`. The GitHub latest endpoint returns that release and reports `draft=false` and `prerelease=false`.
- Independent download verification confirmed APK SHA-256 `EA12B7ECF9BA09D89FCFAB4588E8CDA107DA4EBBBDC54878DF12AC1DB56DE83E`, package `com.darkaxt.nuviodv`, label `NuvioDV`, versionCode `12214`, versionName `0.4.23-nuviodv.1`, ARM64-only native code, APK Signature Scheme v2, signer certificate SHA-256 `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`, and exported `dovi_parse_rpu` plus `dovi_parse_rpu_bin_file` symbols in `libmpv.so`.
- The fork is zero commits behind upstream after the merge; no-update sync run `35336838855` passed without creating another commit or release.
- Issue delta triage identified upstream #1972 (optional smoother ASS motion for Android libmpv) and #1956 (MPV autoplay skips and marks the next episode watched) as playback-relevant candidates. They remain unimplemented because maintenance monitoring does not broaden fork scope automatically.
