# NuvioDV Upstream Maintenance Specification

Authorization: `already_authorized` by the user on 2026-09-12.

## Requirements

- M1: A GitHub Actions workflow must check `NuvioMedia/NuvioMobile` branch `cmp-rewrite` daily.
- M2: When no upstream commit is missing from `Darkaxt/NuvioMobile:cmp-rewrite`, the workflow must not create a commit, push, or release.
- M3: When upstream commits are missing, merge their history into the fork without discarding NuvioDV changes. The workflow may automatically preserve the fork's `iosApp/Configuration/Version.xcconfig` during a conflict limited to that file; any other merge conflict must fail closed for manual repair.
- M4: Each synchronized release must advance both the NuvioDV base semantic version and Android version code. Choose a base version newer than the current NuvioDV base and at least as new as upstream, then use suffix `-nuviodv.1`.
- M5: Before pushing, verify the NuvioDV package identity, app label, local patched libmpv dependency, authenticated-release test, and a full Android debug APK build. A failed invariant or build must prevent the push and release.
- M6: Push the verified sync commit and its version tag atomically, then dispatch the existing authenticated NuvioDV prerelease workflow from that exact tag. Branch-ref propagation must not be allowed to publish an older commit.
- M7: A recurring Codex check must run every three days. It must inspect upstream divergence and daily-workflow/release results; if GitHub automation failed or left commits unsynchronized, it is authorized to diagnose, make the minimal fork-preserving repair, verify, commit, push, and trigger the release itself.
- M8: The three-day check must also inspect new or newly updated open upstream issues for playback problems relevant to NuvioDV, libmpv, Dolby Vision, libplacebo/pink output, hardware decoding, renderer/color-format behavior, subtitles/audio interaction, or long-playback pipeline failure.
- M9: Issue monitoring must not comment on upstream issues or automatically broaden the fork. It reports only evidence-backed candidates worth considering and stays quiet when neither maintenance nor issue triage produces an actionable change.

## Acceptance criteria

- MC1: Version-advance tests fail for same-base pseudo-versions and pass for a higher semantic core plus higher Android version code.
- MC2: The daily workflow parses, has write permissions needed for source sync and release dispatch, and contains fail-closed merge/build behavior.
- MC3: A manual workflow dispatch consumes the currently pending upstream commits, preserves fork invariants, pushes the verified merge, and dispatches a successful authenticated prerelease.
- MC4: A three-day Codex heartbeat is active with the authorized remediation and playback-issue scope.
- MC5: Repository changes and maintenance evidence are committed and pushed to `cmp-rewrite`.

## Stage and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Daily verified upstream sync and release | COMPLETE | M1-M6 | Run 34665705660 merged both pending upstream commits, built and verified the integrated APK, pushed `3dfb5cbc`, and dispatched release run 34665975418; public `0.4.19-nuviodv.1`/`12204` APK independently verified |
| Three-day Codex maintenance and issue triage | COMPLETE | M7-M9 | Active heartbeat `maintain-nuviodv-upstream-fork` runs every three days with authorized remediation, quiet no-change behavior, and issue-delta triage; baseline reviewed all 343 open issues and records #1730 as high relevance while #1675/#1723 remain low confidence |
| Final reconciliation | ACTIVE | M1-M9 | MC1-MC5 checked; blockers and tracked deferrals equal zero |

Blockers: none.

Tracked deferrals: none.
