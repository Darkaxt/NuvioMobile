# Personal libmpv fork integration status

Authoritative specification: `PERSONAL_LIBMPV_FORK_SPEC.md`

## Stage 1 - Dependency integration

- Status: **COMPLETE**
- Requirements: R1, R2, R4
- Acceptance criteria: AC1, AC2, AC3
- Verification required: exact AAR checksum, Gradle dependency resolution,
  affected Android compilation
- Acceptance criteria satisfied: the upstream Maven coordinate is removed;
  the exact public AAR from library commit `a6d4de8` is selected by the existing
  local-AAR mechanism; its SHA-256 matches the specification; and the complete
  NuvioMobile Android source set compiles without player call-site changes.
- Acceptance criteria remaining: none
- Blockers: none
- Tracked deferrals: side-by-side Android identity to Stage 2; README scope and
  provenance presentation to Stage 3; final APK/native inspection to Stage 4

## Stage 2 - Side-by-side Android identity

- Status: **COMPLETE**
- Requirements: R6
- Acceptance criteria: AC6
- Verification required: merged-manifest/application-ID inspection, resource
  label inspection, and generated APK filename inspection
- Acceptance criteria satisfied: the packaged full-debug APK reports application
  ID `com.darkaxt.nuviodv`, every launcher label resolves to `NuvioDV`, provider
  authorities use the new application ID, and the output file is
  `NuvioDV-fullDebug.apk`.
- Acceptance criteria remaining: none
- Blockers: none
- Tracked deferrals: final APK inspection to Stage 4

## Stage 3 - Personal-fork documentation

- Status: **COMPLETE**
- Requirements: R3, R4
- Acceptance criteria: AC4
- Verification required: README and provenance reconciliation against the spec
- Acceptance criteria satisfied: the README identifies the fork as personal and
  unofficial; separates the Dolby Vision and pink-screen concerns; records the
  source repository, commit, successful workflow run, artifact, and checksum;
  documents the side-by-side identity and ARM64/Profile 7 limits; and defines
  the upstream deprecation condition.
- Acceptance criteria remaining: none
- Blockers: none
- Tracked deferrals: final documentation reconciliation to Stage 4

## Stage 4 - Integrated verification

- Status: **COMPLETE**
- Requirements: R5
- Acceptance criteria: AC5 plus final AC1-AC4 and AC6 reconciliation
- Verification required: Android debug APK build and native payload inspection
- Acceptance criteria satisfied: `:androidApp:assembleFullDebug` succeeds; the
  generated APK has SHA-256
  `C8B199080418D0B83F37BDB414D8133D4798F259ECC6B67A6414DBC2D4A352A1`;
  it contains exactly `lib/arm64-v8a/libmpv.so`; and that payload is ELF64
  AArch64 and exports `dovi_parse_rpu`. Final checks also reconfirm the pinned
  AAR checksum, new Android identity, local-AAR selection, absence of the old
  Maven dependency, unchanged player call sites, and documentation requirements.
- Acceptance criteria remaining: none
- Blockers: none
- Tracked deferrals: none

## Stage 1-4 reconciliation

- Requirements R1-R6: satisfied and verified
- Acceptance criteria AC1-AC6: satisfied and verified
- Remaining blockers: none
- Remaining tracked deferrals: none
- Explicitly out of scope: device playback itself, app-store/iOS publication,
  full Profile 7 FEL claims, and mpvEx feature expansion

## Stage 5 - Signed tablet-validation prerelease

- Status: **ACTIVE**
- Requirements: R7
- Acceptance criteria: AC7
- Verification required: protected persistent key creation, local signed APK
  verification, successful public Android-only workflow, and independent
  verification of the downloaded GitHub release asset
- Acceptance criteria satisfied: a dedicated 4096-bit RSA signing identity is
  retained locally at `C:\Users\darka\.android\nuviodv-release.jks` with its
  password stored only as a DPAPI-protected recovery record; four required
  GitHub Actions secrets are configured; the Android-only workflow is defined;
  and a locally signed ARM64 release APK for `0.4.17-nuviodv.1`/`12201` passed
  package, label, V2 signature, signer-certificate, ELF architecture, unique
  libmpv payload, and `dovi_parse_rpu` checks.
- Acceptance criteria remaining: successful public workflow publication and
  independent verification of the downloaded release asset
- Blockers: none
- Tracked deferrals: none

## Revised final reconciliation

- Requirements R1-R6: satisfied and verified
- Requirement R7: active in Stage 5 following the owner's scope correction
- Remaining blockers: none
- Remaining tracked deferrals: none
