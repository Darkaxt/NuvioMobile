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

## Acceptance Criteria

1. A focused repository test proves stale collection rows are removed and current rows follow collection order.
2. The same test proves unrelated addon-row state remains unchanged.
3. General > Layout > Collections renders the rebuild action beside Copy and Import.
4. Android compilation succeeds.
5. The verified implementation is committed to `cmp-rewrite`; publishing a release is out of scope.

## Stages

| Stage | Status | Acceptance criteria |
| --- | --- | --- |
| Repository behavior | COMPLETE | 1, 2 |
| Collections toolbar | COMPLETE | 3 |
| Integrated verification and commit | COMPLETE | 4, 5 |

## Verification

- `HomeCatalogSettingsRepositoryTest` passes, including stale-row removal, collection-order rebuilding, and preservation of addon-row state.
- `:androidApp:assembleFullDebug` succeeds with the new toolbar action and string resource.
- `git diff --check` reports no whitespace errors.
