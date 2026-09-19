# NuvioDV Continue Watching Metadata Scheduling

## Authorization

Status: `already_authorized`

The user reported persistent missing Continue Watching portraits after the previous portrait-renderer fix, asked why metadata work was not queued and limited per second, and authorized the scheduling fix. The existing release workflow remains part of the defect-remediation outcome.

## Requirements

- `CWM-1`: Every add-on metadata HTTP request made through `MetaDetailsRepository`, including Continue Watching, Next Up, watched-badge, playback, and interactive-detail callers, must use one shared request scheduler.
- `CWM-2`: The shared scheduler must start at most two add-on metadata HTTP requests per second, without an initial or retry burst.
- `CWM-3`: Concurrent `MetaDetailsRepository.fetch` calls for the same media key must share one in-flight result instead of issuing duplicate provider requests.
- `CWM-4`: Cancellation must release scheduler and in-flight state so later requests cannot become permanently blocked.
- `CWM-5`: Existing successful metadata caching and provider fallback behavior must remain intact.
- `CWM-6`: Publish the verified fix as the next normal signed NuvioDV Android release.

## Acceptance Criteria

1. A deterministic focused test proves that permits are spaced by at least 500 ms, including concurrent waiters.
2. A focused test proves that cancellation does not strand the scheduler lock.
3. A repository audit confirms that all add-on metadata network calls funnel through the shared scheduler.
4. A focused test proves that same-key concurrent fetch leases have exactly one owner and share one result.
5. Focused tests and the applicable Android debug build pass.
6. The signed public release reports a version newer than `0.4.25-nuviodv.2` and is not marked as a prerelease.

## Staged Plan And Reconciliation Ledger

### Stage 1: Shared scheduling and in-flight coalescing

Status: `COMPLETE`

Requirements: `CWM-1` through `CWM-5`

Objective:

- Add focused failing tests for deterministic rate spacing, cancellation recovery, and same-key request coalescing.
- Route the single add-on metadata network boundary through a shared two-requests-per-second scheduler.
- Coalesce same-key `fetch` calls while preserving cache and fallback behavior.
- Audit every metadata caller and network boundary.

Acceptance evidence required:

- The focused tests fail for the missing behavior before production changes and pass afterward.
- The add-on metadata call-site audit finds no network path bypassing the scheduler.
- The Android debug build succeeds.

Evidence:

- `MetadataRequestCoordinatorTest` failed before production implementation because the shared limiter and in-flight coordinator did not exist, then passed after implementation.
- The focused scheduler, Continue Watching artwork, and RPDB Continue Watching test classes pass under `:composeApp:testAndroidHostTest`.
- The scheduler spaces starts by 500 ms, releases its queue lock when a waiter is cancelled, and coalesces same-key fetches behind one owner.
- The repository audit finds one add-on metadata resource construction and one corresponding `fetchAddonResponseText` call in `MetaDetailsRepository`; both Continue Watching pipelines and every other `MetaDetailsRepository.fetch` caller reach that boundary.
- Queue waiting occurs before the provider request timeout begins, so a long queue does not cause requests to expire before receiving a permit.
- `:androidApp:assembleFullDebug` completes successfully.
- `git diff --check` reports no whitespace errors.

Blockers: none.

Tracked deferrals: none.

### Stage 2: Normal signed release

Status: `COMPLETE`

Requirements: `CWM-6`

Acceptance evidence required:

- The verified source is committed and pushed to `cmp-rewrite`.
- The normal release workflow succeeds for the exact source commit.
- The public release and APK report the expected NuvioDV version, version code, package, signer, and checksum.

Evidence:

- Source commit `4424ff284db3600361175785911765fcc457933f` is pushed to `cmp-rewrite`.
- GitHub Actions run `35463993025` completed successfully against that exact source commit and published the normal release.
- Public release `v0.4.25-nuviodv.3` is neither a draft nor a prerelease.
- The independently downloaded public APK reports package `com.darkaxt.nuviodv`, label `NuvioDV`, version name `0.4.25-nuviodv.3`, and version code `12224`.
- The public APK SHA-256 is `49f14867e7e753c5420d747b205755a3897cad0a0293eb8d573ccd6e448377af`, matching the GitHub release asset digest.
- APK Signature Scheme v2 verification succeeds with certificate SHA-256 `1fb94424753a90f993c678b6fa4322579253bb303f22c335db395a9e2557d571`.
- The APK advertises only `arm64-v8a`, contains exactly one `lib/arm64-v8a/libmpv.so`, and that library exposes the `dovi_parse_rpu` symbol.

Blockers: none.

Tracked deferrals: none.

## Final Reconciliation

Status: `COMPLETE`

Blockers: none.

Tracked deferrals: none.
