# NuvioDV Version Scheme Correction Specification

Authorization: `already_authorized` by the user's correction on 2026-09-12.

## Requirements

- V1: The semantic core before `-nuviodv` must exactly represent the current upstream Nuvio release version.
- V2: When upstream remains on the same semantic core, each distinct NuvioDV build increments only the fork suffix.
- V3: When upstream advances its semantic core, adopt that core and reset the fork suffix to `1`.
- V4: Treat an upstream semantic core older than the current fork core as an invalid state and fail closed instead of inventing a newer Nuvio core.
- V5: Correct the playback-details build lineage to `0.4.17-nuviodv.5`; advance Android versionCode monotonically for its replacement release.
- V6: Prevent the invalid `0.4.18` through `0.4.21` fork releases from remaining authoritative for update clients, and publish the corrected build as a normal release.

## Acceptance criteria

- VC1: Version tests prove same-core suffix increment, newer-upstream suffix reset, and older-upstream rejection.
- VC2: The daily upstream workflow uses the corrected version function and its contract tests pass.
- VC3: The corrected source reports `MARKETING_VERSION=0.4.17-nuviodv.5` and a versionCode greater than `12206`.
- VC4: The replacement normal release is public, is not a prerelease, and its public APK independently verifies version, package, signer, ABI, libdovi payload, and checksum.
- VC5: Invalid releases no longer supersede the corrected release in GitHub's public release feed.
- VC6: All repository changes are committed and pushed to `cmp-rewrite`.

## Stages and reconciliation ledger

| Stage | Status | Requirements | Verification |
| --- | --- | --- | --- |
| Correct version contract and automation | COMPLETE | V1-V4 | Five focused version tests and six workflow contract tests pass; same-base increment, upstream reset, and regression rejection verified |
| Correct build identity | COMPLETE | V5 | Debug APK verifies package `com.darkaxt.nuviodv`, versionCode `12207`, versionName `0.4.17-nuviodv.5`, label `NuvioDV`, and expected debug ABIs |
| Repair public release lineage | COMPLETE | V6 | Run `34690741856`; corrected normal release `v0.4.17-nuviodv.5` is GitHub latest; erroneous `.21` retained as superseded prerelease; public APK independently verified |

Blockers: none.

Tracked deferrals: none.

## Final release evidence

- Corrected normal release: `v0.4.17-nuviodv.5`, built from `61e4eb15f69b615b92f09aabd36337c6bb2fce84`.
- Public APK identity: package `com.darkaxt.nuviodv`, versionCode `12207`, versionName `0.4.17-nuviodv.5`, label `NuvioDV`, ABI `arm64-v8a`.
- APK SHA-256: `13D53F231353AD1BECAD77A6FA2EE69B76338BF3E15DF3C871BEBF83B83A1231`.
- Signing certificate SHA-256: `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`.
- Public `libmpv.so` exports `dovi_parse_rpu` and `dovi_parse_rpu_bin_file`.
- GitHub's latest-release API resolves to the corrected normal release; `v0.4.21-nuviodv.1` is marked as a superseded prerelease rather than deleted.
