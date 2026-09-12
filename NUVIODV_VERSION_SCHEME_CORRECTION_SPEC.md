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
| Repair public release lineage | ACTIVE | V6 | GitHub release/API and independent public APK verification |

Blockers: none.

Tracked deferrals: none.
