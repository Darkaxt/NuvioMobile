# NuvioDV Collection Layout Rebuild Specification

Authorization: requested by the user on 2026-09-18.

## Objective

Add a one-click action to General > Layout > Collections that rebuilds Home Layout collection rows from the current collection list without modifying collection definitions.

## Requirements

- Add a rebuild/reload icon beside the existing Copy JSON and Import actions.
- Treat the current collection list and its order as authoritative for collection rows in Home Layout.
- Remove stale `collection_*` Home Layout preferences whose collection no longer exists.
- Preserve addon catalog rows, collection contents, collection artwork, row enabled state, and custom titles.
- Persist and sync the repaired Home Layout payload without writing to collection sync storage.
- Publish the verified change as the next normal signed ARM64 NuvioDV release without claiming the newer unsynchronized upstream `0.4.24` base.

## Acceptance Criteria

1. A focused repository test proves stale collection rows are removed and current rows follow collection order.
2. The same test proves unrelated addon-row state remains unchanged.
3. General > Layout > Collections renders the rebuild action beside Copy and Import.
4. Android compilation succeeds.
5. The verified implementation is committed and pushed to `cmp-rewrite`.
6. Normal release `v0.4.23-nuviodv.7` is published from the exact verified commit with Android version code `12220`.
7. The published APK independently verifies package `com.darkaxt.nuviodv`, app label `NuvioDV`, ARM64-only native payload, established signing identity, and patched libdovi symbols.

## Stages

| Stage | Status | Acceptance criteria |
| --- | --- | --- |
| Repository behavior | COMPLETE | 1, 2 |
| Collections toolbar | COMPLETE | 3 |
| Integrated verification and commit | COMPLETE | 4 |
| Signed release delivery | COMPLETE | 5, 6, 7 |

## Verification

- `HomeCatalogSettingsRepositoryTest` passes, including stale-row removal, collection-order rebuilding, and preservation of addon-row state.
- `:androidApp:assembleFullDebug` succeeds with the new toolbar action and string resource.
- `git diff --check` reports no whitespace errors.
- Source commit `67c366b3d78978f0396d61718bb4a6ff65f5386c` is pushed to `origin/cmp-rewrite`.
- GitHub Actions run `35394706431` built, verified, and published normal release `v0.4.23-nuviodv.7` from that exact source commit.
- Independently downloaded APK SHA-256 is `103ed312c211791a662301fbf474911343ee640438d43b8edcc8de1e6424c670`, matching the GitHub release digest.
- Independent APK inspection verifies package `com.darkaxt.nuviodv`, version name `0.4.23-nuviodv.7`, version code `12220`, app label `NuvioDV`, only `arm64-v8a` native libraries, one `libmpv.so`, signer SHA-256 `1fb94424753a90f993c678b6fa4322579253bb303f22c335db395a9e2557d571`, and exported `dovi_parse_rpu`, `pl_shader_dovi_reshape`, and `pl_hdr_metadata_from_dovi_rpu` symbols.
