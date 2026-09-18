# NuvioDV Native Trakt Collections Implementation Plan

Authoritative specification: `NUVIODV_NATIVE_TRAKT_COLLECTIONS_SPEC.md`.

Only one stage may be active. A stage advances only after its assigned acceptance criteria have fresh verification.

## Stage 1: Source Model And Routing

Status: `COMPLETE`

- Add failing serialization, compatibility, validation, and route-key tests.
- Introduce explicit Trakt collection source types with legacy public-list inference.
- Route every Trakt collection source through one resolver boundary.
- Close with the focused source-model test set.

## Stage 2: Account Catalogue Resolution

Status: `COMPLETE`

- Add endpoint/mapping tests for recommendations, watchlist, calendar, up-next, and recently aired.
- Implement authenticated resolution through the active profile's `TraktAuthRepository`.
- Reuse shared Trakt models and progress logic where they match the required semantics.
- Close with focused resolver tests.

## Stage 3: Editor Integration

Status: `COMPLETE`

- Add first-class account catalogue choices to the Trakt source picker.
- Preserve the existing public-list workflow.
- Close with state-level tests and a focused compilation check.

## Stage 4: Collection Migration

Status: `COMPLETE`

- Generate the dated reconciled import artifact from the current reconciled collection.
- Replace exactly seven AIOMetadata Trakt sources.
- Verify semantic preservation, catalogue ordering, `By Decade`, and `Anime` placement.

## Stage 5: Documentation And Release

Status: `ACTIVE`

- Update README and version metadata.
- Run focused tests and the integrated Android debug build.
- Commit and push the exact verified source.
- Publish and independently verify normal release `v0.4.23-nuviodv.2`.

## Stage 6: Final Reconciliation

Status: `NOT STARTED`

- Reconcile every T requirement and TC acceptance criterion.
- Record final evidence, blockers, and deferrals in the specification.
