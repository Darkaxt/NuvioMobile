# NuvioDV Upstream Maintenance Specification

Authorization: `already_authorized` by the user on 2026-09-12.

## Requirements

- M1: A GitHub Actions workflow must check `NuvioMedia/NuvioMobile` branch `cmp-rewrite` daily.
- M2: When no upstream commit is missing from `Darkaxt/NuvioMobile:cmp-rewrite`, the workflow must not create a commit, push, or release.
- M3: When upstream commits are missing, merge their history into the fork without discarding NuvioDV changes. The workflow may automatically preserve the fork's `iosApp/Configuration/Version.xcconfig` during a conflict limited to that file; any other merge conflict must fail closed for manual repair.
- M4: Each synchronized release must retain the exact current upstream semantic version as its base and advance the Android version code. If upstream remains on the same version, increment only the `-nuviodv.#` fork counter; if upstream advances its version, adopt it and reset the fork counter to `1`; fail closed if upstream appears older than the fork base.
- M5: Before pushing, verify the NuvioDV package identity, app label, local patched libmpv dependency, authenticated-release test, and a full Android debug APK build. A failed invariant or build must prevent the push and release.
- M6: After pushing the verified sync commit, dispatch the authenticated NuvioDV prerelease workflow with that exact commit as an explicit checkout input. Branch-ref propagation must not be allowed to publish an older commit.
- M7: A recurring Codex check must run every three days. It must inspect upstream divergence and daily-workflow/release results; if GitHub automation failed or left commits unsynchronized, it is authorized to diagnose, make the minimal fork-preserving repair, verify, commit, push, and trigger the release itself.
- M8: The three-day check must also inspect new or newly updated open upstream issues for playback problems relevant to NuvioDV, libmpv, Dolby Vision, libplacebo/pink output, hardware decoding, renderer/color-format behavior, subtitles/audio interaction, or long-playback pipeline failure.
- M9: Issue monitoring must not comment on upstream issues or automatically broaden the fork. It reports only evidence-backed candidates worth considering and stays quiet when neither maintenance nor issue triage produces an actionable change.

## Acceptance criteria

- MC1: Version-advance tests prove same-base fork-counter increments, newer-upstream resets, older-upstream rejection, and a higher Android version code.
- MC2: The daily workflow parses, has write permissions needed for source sync and release dispatch, and contains fail-closed merge/build behavior.
- MC3: A manual workflow dispatch consumes the currently pending upstream commits, preserves fork invariants, pushes the verified merge, and dispatches a successful authenticated prerelease.
- MC4: A three-day Codex heartbeat is active with the authorized remediation and playback-issue scope.
- MC5: Repository changes and maintenance evidence are committed and pushed to `cmp-rewrite`.

## Stage and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Daily verified upstream sync and release | COMPLETE | M1-M6 | Runs 34665705660 and 34666617695 consumed the initial pending commits; source-SHA input fixes branch-ref propagation race; run 34667333366 verified the unchanged-upstream no-op path; version contract corrected in `61e4eb15`; on 2026-09-13 run 34723027169 failed closed on four overlapping player-settings files plus the expected version conflict, after which the manual repair retained both upstream settings and NuvioDV playback details, passed focused tests and an integrated APK build, and prepared `0.4.18-nuviodv.1`/`12208` |
| Three-day Codex maintenance and issue triage | COMPLETE | M7-M9 | Active heartbeat `maintain-nuviodv-upstream-fork` runs every three days with authorized remediation, quiet no-change behavior, and issue-delta triage; baseline reviewed all 343 open issues and records #1730 as high relevance while #1675/#1723 remain low confidence |
| Final reconciliation | COMPLETE | M1-M9 | MC1-MC5 satisfied; fork contains current upstream, workflows and heartbeat active, public release verified, blockers and tracked deferrals equal zero |

Blockers: none.

Tracked deferrals: none.

## 2026-09-13 sync incident

- Upstream advanced by 33 commits after the preceding scheduled run and released Nuvio `0.4.18`.
- The immediate manual dispatch failed closed before any push or release because upstream's loading-status and pause-overlay settings overlapped NuvioDV's playback-details setting in four repository/storage files; `Version.xcconfig` was the fifth conflict.
- Manual resolution retained all three settings across the shared repository plus Android and iOS storage/sync paths.
- Focused version/workflow contracts and the three affected Android player-settings tests passed; the integrated full debug APK built successfully as `0.4.18-nuviodv.1` with versionCode `12208`.
