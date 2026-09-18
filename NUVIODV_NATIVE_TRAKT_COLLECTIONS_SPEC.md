# NuvioDV Native Trakt Collections Specification

Authorization: `already_authorized` by the user on 2026-09-18.

## Objective

Add first-class authenticated Trakt catalogue sources to NuvioDV, migrate the seven Trakt-backed rows in the user's reconciled Nuvio collection away from AIOMetadata, document the feature, and publish a verified normal NuvioDV release.

## Requirements

- T1: `CollectionSource` must represent Trakt public lists and authenticated account catalogues as explicit, serializable source types rather than overloading a list identifier.
- T2: Existing imported Trakt public-list sources that contain `traktListId` but no source-type field must remain valid and retain their current behavior.
- T3: Authenticated Trakt catalogue resolution must reuse the active profile's existing `TraktAuthRepository` authorization and refresh path. It must not add a second login flow or embed user credentials/tokens.
- T4: Native catalogue resolution must preserve these seven source variants: movie recommendations, movie watchlist, series recommendations, series up next, series recently aired/unwatched, series calendar, and series watchlist.
- T5: Native Trakt sources must resolve through one collection-source boundary with stable route keys, predictable pagination, existing Nuvio metadata models, and actionable unauthenticated/error results.
- T6: The collection editor must expose authenticated Trakt account catalogues as normal Trakt source choices while retaining public-list search, import, editing, and sorting behavior.
- T7: Exported/imported collection JSON must round-trip the new Trakt source fields and validate list identifiers only for public-list sources.
- T8: Produce a new reconciled collection JSON by replacing only the seven `aio-metadata` Trakt sources in `Discover > For You` with native NuvioDV Trakt sources. Preserve all other source wiring, folders, assets, and collection order; preserve `By Decade` newest-to-oldest and keep `Anime` immediately below `Genres`.
- T9: Update the README to describe the native Trakt collection capability, authentication dependency, supported catalogue types, and import artifact.
- T10: Publish a new normal GitHub release from the exact verified commit while preserving package `com.darkaxt.nuviodv`, app name `NuvioDV`, ARM64-only packaging, signing identity, and the patched libmpv/libdovi integration.
- T11: Advance the same-base fork version from `0.4.23-nuviodv.1` to `0.4.23-nuviodv.2` and increment Android `versionCode` beyond `12214`.
- T12: Native account-source exports must remain importable through the current Nuvio configuration website, whose validator requires a numeric `traktListId` for every Trakt source, without changing account-source semantics or colliding preservation keys.
- T13: Publish normal patch release `v0.4.23-nuviodv.3` with Android `versionCode` greater than `12215`, preserving the package, label, ARM64 payload, signing identity, and patched player integration verified for the initial native Trakt release.

## Acceptance Criteria

- TC1: Focused serialization and validation tests prove legacy public-list compatibility, all account source-type round trips, list-ID validation boundaries, and distinct stable route keys.
- TC2: Focused resolver tests prove endpoint selection, authorization use, pagination, mapping, ordering, and failure behavior for all seven migrated catalogue variants.
- TC3: Editor tests or equivalent state-level tests prove account catalogue sources can be added and edited without requiring a public-list ID while public-list behavior remains intact.
- TC4: The integrated Android debug build succeeds after the feature is connected through `FolderDetailRepository` and the collection editor.
- TC5: The generated collection file parses, contains exactly seven native Trakt replacements and zero `aio-metadata` Trakt catalogues, preserves all unrelated source records byte-for-byte at the semantic JSON level, preserves `By Decade` newest-to-oldest, and keeps `Anime` immediately below `Genres`.
- TC6: The README identifies the native Trakt collection support and the exact Windows path of the generated import artifact.
- TC7: Repository changes are committed and pushed to `cmp-rewrite`.
- TC8: The normal GitHub release `v0.4.23-nuviodv.2` is published from the exact verified source commit and is returned as the latest release.
- TC9: The published APK independently verifies package, label, version name/code, ARM64-only payload, expected signing certificate, and libdovi symbols.
- TC10: Final reconciliation records zero blockers and zero unresolved tracked deferrals.
- TC11: Exported account sources contain compatibility value `traktListId: 0`, public lists retain their real positive IDs, account-source preservation keys distinguish source type/media/calendar window, and the reconciled JSON passes the current website validator.
- TC12: Release `v0.4.23-nuviodv.3` is published from the exact verified compatibility-fix commit, is returned as the latest normal release, and its APK independently passes the established package/version/ABI/signing/libdovi checks.

## Source Semantics

| Source type | Media | Trakt behavior |
| --- | --- | --- |
| `recommendations` | movie / series | Personalized recommendations from `/recommendations/movies` or `/recommendations/shows` |
| `watchlist` | movie / series | Active user's `/sync/watchlist/movies` or `/sync/watchlist/shows` |
| `up_next` | series | Next aired unwatched episode for active watched shows, excluding hidden/dropped shows |
| `unwatched` | series | Recently aired unwatched episodes for active watched shows, excluding hidden/dropped shows |
| `calendar` | series | Active user's recently aired calendar window, grouped by show |
| `public_list` | movie / series | Existing list-ID-based public-list behavior |

The serialized field is `traktSourceType`. Missing `traktSourceType` plus a non-blank `traktListId` is interpreted as `public_list` for backward compatibility.

## Stages And Reconciliation Ledger

| Stage | Status | Requirements | Acceptance criteria |
| --- | --- | --- | --- |
| Authoritative contract | COMPLETE | T1-T11 | Scope, source semantics, migration invariants, release target, and verification are explicit |
| Source model and routing | COMPLETE | T1, T2, T5, T7 | TC1 passed in `CollectionSourceSerializationTest`; legacy inference, all seven account shapes, validation boundaries, and route identity verified |
| Account catalogue resolution | COMPLETE | T3-T5 | TC2 passed in `TraktAccountCatalogClientTest`; all seven routes, pagination, mapping, calendar grouping, dropped-show filtering, partial-failure behavior, and profile OAuth boundary verified |
| Editor integration | COMPLETE | T6, T7 | TC3 passed in `CollectionEditorTraktSourceTest`; account/public-list mode selection, dual-media creation, series-only constraints, calendar bounds, and legacy public-list edit state verified |
| Collection migration | COMPLETE | T8 | TC5 passed for `nuvio-collections-kaptain-mega-hybrid-2026-09-18-nuviodv-trakt.reconciled.json`; seven native sources, zero AIOMetadata Trakt refs, unrelated semantic JSON preserved, decade order and Anime placement verified |
| Documentation and release | COMPLETE | T9-T11 | TC4 and TC6-TC9 passed; full debug build succeeded, README/version updated, source `83f45109c6ab570744a465cf69333c66b3817be9` pushed, and normal release `v0.4.23-nuviodv.2` independently verified |
| Final reconciliation | COMPLETE | T1-T11 | TC10 passed for the initial native Trakt implementation, with zero blockers and zero tracked deferrals at that boundary |
| Website import compatibility | ACTIVE | T12, T13 | TC11, TC12; repaired artifact passes the website rule, app export/preservation tests pass, patch release pending |

Blockers: the `v0.4.23-nuviodv.2` import artifact is rejected by the current website because explicit account sources omit its required numeric `traktListId` compatibility field.

Tracked deferrals: none.

## Verification Evidence

- Focused Android host tests passed for source serialization, public-list compatibility, account catalogue resolution, OAuth-header forwarding, and editor source construction.
- `:androidApp:assembleFullDebug` completed successfully with package `com.darkaxt.nuviodv`, label `NuvioDV`, version `0.4.23-nuviodv.2`, and version code `12215`.
- Reconciled collection: `C:\Users\darka\Documents\Projects\Stremio Add-on Tester\output\nuvio-collections-kaptain-mega-hybrid-2026-09-18-nuviodv-trakt.reconciled.json`.
- Collection SHA-256: `08140C53D2842DAABD21D4DC5C219B73F0DD624FAB2D4CBE8EAB00D76DF1F3D8`.
- Release workflow: `https://github.com/Darkaxt/NuvioMobile/actions/runs/35344780813`.
- Release: `https://github.com/Darkaxt/NuvioMobile/releases/tag/v0.4.23-nuviodv.2`.
- Release source: `83f45109c6ab570744a465cf69333c66b3817be9`.
- Published APK: `NuvioDV-0.4.23-nuviodv.2-arm64-v8a.apk`.
- APK SHA-256: `0B0E000E9FA9F2B6CE9C6D0E28AAA226425DCA75CF3466F7443B4711AD3BA7DD`.
- Signing certificate SHA-256: `1FB94424753A90F993C678B6FA4322579253BB303F22C335DB395A9E2557D571`, matching the previous normal release.
- Independent APK inspection confirmed ARM64-only native payload, one `lib/arm64-v8a/libmpv.so`, and the `dovi_parse_rpu` symbol.
- Final collection validation confirmed 22 collections, exactly seven native Trakt sources in `Discover > For You`, zero legacy AIOMetadata Trakt references, newest-to-oldest `By Decade`, `Anime` immediately after `Genres`, and zero movie-after-series ordering violations.
- The repository-wide Android host test task has six unrelated download-test failures. Running the exact failing test classes at pre-feature commit `cac0a6c7` reproduces the same six failures, while the Trakt commit changes no download implementation or test files; these are verified baseline failures rather than regressions from this work.
