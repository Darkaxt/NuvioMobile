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
| Build and publish replacement prerelease | COMPLETE | R4, R5 | Run 34663828236 passed generated-config, APK, native, signature, upload, and publication checks; independent asset verification passed |
| Final reconciliation | COMPLETE | R1-R6 | AC1-AC5 satisfied; device login verification remains user-owned under R6 |

Blockers: none.

Tracked deferrals: none.

## Final evidence

- Commit: `11a3a98c3d609c8209293f321a8c74010bf568e7`
- Workflow: `https://github.com/Darkaxt/NuvioMobile/actions/runs/34663828236`
- Prerelease: `https://github.com/Darkaxt/NuvioMobile/releases/tag/v0.4.17-nuviodv.2`
- APK: `NuvioDV-0.4.17-nuviodv.2-arm64-v8a.apk`
- APK SHA-256: `9FA5031A5ABB56B6D91C9DF0B5FBFDDB8532DE294683D94BA9CD35FC5CCF4715`
- Independent verification: package `com.darkaxt.nuviodv`, version `0.4.17-nuviodv.2`/`12202`, label `NuvioDV`, ARM64-only payload, matching persistent signer, AArch64 `libmpv`, `dovi_parse_rpu`, and embedded Supabase/Trakt/Simkl configuration.
- Final blockers: none.
- Final tracked deferrals: none.
