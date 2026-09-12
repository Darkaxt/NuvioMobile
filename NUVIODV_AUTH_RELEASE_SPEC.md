# NuvioDV Authenticated Release Specification

Authorization: `already_authorized` by the user on 2026-09-12.

## Requirements

- R1: NuvioDV release builds must contain the official Nuvio backend URL, public anonymous key, and fallback URL required by Nuvio account authentication.
- R2: NuvioDV release builds must contain the Trakt client ID and secret and the Simkl client ID required by the existing tracking-provider login implementations.
- R3: The release workflow must fail before building or publishing when any R1 or R2 value, signing value, or decoded runtime property is absent.
- R4: The replacement release must retain package `com.darkaxt.nuviodv`, app name `NuvioDV`, ARM64-only packaging, the existing NuvioDV signing identity, and the patched `libmpv`/libdovi integration.
- R5: Publish a new GitHub prerelease with a version newer than `0.4.17-nuviodv.1`; do not replace or mutate the existing release.
- R6: Device login verification is owned by the user after publication.

## Acceptance criteria

- AC1: A focused automated test proves missing or incomplete runtime configuration is rejected and complete configuration is written without leaking values to logs.
- AC2: Generated Supabase, Trakt, and Simkl configuration files contain non-empty required constants during the release build.
- AC3: The signed published APK independently verifies the required package, app label, version, ARM64 `libmpv`, libdovi symbol, checksum, and signing certificate.
- AC4: The new prerelease and APK are publicly retrievable from `Darkaxt/NuvioMobile`.
- AC5: Repository changes are committed and pushed to `cmp-rewrite`.

## Stages and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Restore authenticated release configuration | COMPLETE | R1, R2, R3 | Red test rejected the absent configuration script; green test rejects incomplete properties and accepts complete sanitized properties; GitHub runtime secret configured from official embedded client values |
| Build and publish replacement prerelease | ACTIVE | R4, R5 | Generated-config validation, GitHub Actions run, downloaded-asset verification |
| Final reconciliation | NOT STARTED | R1-R6 | AC1-AC5 checked; blockers and tracked deferrals equal zero |

Blockers: none.

Tracked deferrals: none.
