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
| Signed release delivery | ACTIVE | 5, 6, 7 |

## Verification

- `HomeCatalogSettingsRepositoryTest` passes, including stale-row removal, collection-order rebuilding, and preservation of addon-row state.
- `:androidApp:assembleFullDebug` succeeds with the new toolbar action and string resource.
- `git diff --check` reports no whitespace errors.
