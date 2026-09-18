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
| Documentation and release | ACTIVE | T9-T11 | TC4, TC6-TC9 |
| Final reconciliation | NOT STARTED | T1-T11 | TC10 |

Blockers: none.

Tracked deferrals: none.
