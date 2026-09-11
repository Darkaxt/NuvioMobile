# Personal libmpv fork integration specification

## Status and authorization

- Implementation is already authorized by the repository owner's request to proceed with fixing NuvioMobile.
- This document is the authoritative specification for the current fork scope.

## Requirements

### R1. Patched Android libmpv dependency

The Android target must use the ARM64 AAR produced by
[`Darkaxt/mpv-android-libdovi`](https://github.com/Darkaxt/mpv-android-libdovi)
at commit `a6d4de8b2109347e07dcd2daef258deee9a97e29`, rather than
`io.github.abdallahmehiz:mpv-android-lib:0.1.12`.

The integrated AAR must have SHA-256
`B266C9F5ED940B761DA572F1496FCF2152FE624CDFD42354B33BA5C9E3FC8721`.

### R2. Existing player behavior

The existing Android libmpv player selection, settings, and `is.xyz.mpv` call
sites must remain unchanged. This stage replaces the compatible native/library
implementation; it does not add a new player or route around the existing
selection.

### R3. Personal-fork scope

The README must state that this is a personal fork covering two independent
player concerns:

1. improved Dolby Vision handling through the patched libmpv stack; and
2. the included libplacebo fix relevant to the late-playback pink-screen issue,
   which is not being treated as a Dolby Vision issue.

It must also state that the fork should be deprecated when upstream covers the
same gaps, unless its scope is explicitly expanded later.

### R4. Reproducibility and attribution

The repository must record the library source repository, source commit,
successful GitHub Actions run, artifact name, and AAR checksum. The vendored
binary must remain traceable to that record.

### R5. Verification

The Android project must resolve and compile against the vendored AAR without
the upstream Maven dependency. The generated APK must contain the patched
ARM64 native payload, including the libdovi symbol used by the library build.

### R6. Side-by-side Android identity

The Android fork must install alongside the standard Nuvio app by using
`com.darkaxt.nuviodv` as its application ID. Its user-visible Android name must
be `NuvioDV`, and generated APK filenames must begin with `NuvioDV-`.

The existing Kotlin namespace and source packages may remain `com.nuvio.app`;
renaming them is not required for Android package isolation and would create
unnecessary source churn.

## Explicit limits

- ARM64 Android only for the libmpv native payload.
- No claim of full Dolby Vision Profile 7 FEL decoding.
- No mpvEx features or generalized player expansion.
- No iOS/MPVKit changes.
- No Kotlin namespace or source-package rename.
- No GitHub release, store publication, or Maven publication in this scope.
- Device playback validation is intentionally left to the repository owner.

## Acceptance criteria

- AC1: no production Gradle dependency on
  `io.github.abdallahmehiz:mpv-android-lib` remains.
- AC2: the exact pinned AAR is tracked and selected by Android `commonMain`'s
  existing local-AAR mechanism.
- AC3: existing Android libmpv source call sites compile without adaptation.
- AC4: README and provenance documentation satisfy R3 and R4.
- AC5: an Android debug APK builds and its ARM64 `libmpv.so` exposes
  `dovi_parse_rpu`.
- AC6: the generated APK has application ID `com.darkaxt.nuviodv`, presents
  itself as `NuvioDV`, and uses a filename beginning with `NuvioDV-`.
