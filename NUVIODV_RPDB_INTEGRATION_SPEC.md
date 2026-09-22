# NuvioDV RPDB Portrait Integration

## Authorization

Status: `already_authorized`

The user requested RPDB support under General > Integrations and specified that a custom API key must be supported with `t0-free-rpdb` as the fallback key.

## Requirements

- `RPDB-1`: Add an RPDB settings page under General > Integrations.
- `RPDB-2`: RPDB is disabled by default and can be enabled independently of TMDB metadata enrichment.
- `RPDB-3`: Accept an optional custom RPDB API key. When it is blank, use `t0-free-rpdb`.
- `RPDB-4`: Apply RPDB only to portrait artwork for movie and series `MetaPreview` items with compatible IMDb or TMDB IDs.
- `RPDB-5`: Leave landscape artwork, logos, folder covers, unsupported IDs, and non-movie/series items unchanged.
- `RPDB-6`: If an RPDB image request fails, retry display with the item's original poster URL.
- `RPDB-7`: Keep the custom API key profile-scoped and local-only. Exclude it from both ordinary profile-settings payloads and provider-credential synchronization so hosted sync never reads, writes, clears, or rejects it.
- `RPDB-8`: Changing RPDB settings must take effect when returning to portrait-bearing screens without requiring an application restart.
- `RPDB-9`: Cover the resolver, settings policy, and credential handling with focused tests.
- `RPDB-10`: Publish the verified integration as a signed NuvioDV Android release with a version newer than the installed test build.
- `RPDB-11`: Display the branded RPDB icon in the General > Integrations row on phone and tablet layouts.
- `RPDB-12`: Inventory every portrait-bearing production renderer and ensure compatible movie/series portraits use the shared RPDB resolver, including portrait-style Continue Watching cards whose model is not `MetaPreview`.
- `RPDB-13`: Continue Watching portrait cards must preserve the original artwork as the display fallback when the RPDB request fails.
- `RPDB-14`: Continue Watching full-background Card artwork, cloud-library artwork, unsupported identifiers, and non-movie/series items must remain unchanged.
- `RPDB-15`: The artwork strip inside the Continue Watching Wide layout must preserve Nuvio's existing artwork priority. With episode thumbnails enabled, an available episode thumbnail remains primary. RPDB may replace a selected portrait poster, but must not change an episode-thumbnail selection into a series-poster selection. Existing fallbacks remain available when the preferred artwork is absent.
- `RPDB-16`: Opening General > Integrations on Android must not decode the RPDB SVG through the Compose multiplatform Android painter. Android must use a platform-supported packaged drawable while iOS retains the shared SVG asset.
- `RPDB-17`: Continue Watching must preserve episode-thumbnail priority while resolving a failing poster-cache wrapper to its supplied valid fallback image URL.

## Acceptance Criteria

1. General > Integrations contains an RPDB entry on phone and tablet layouts.
2. The RPDB page exposes an enable switch and optional masked custom-key field, and explains the public fallback.
3. With RPDB disabled, existing portrait URLs are unchanged.
4. With RPDB enabled and no custom key, IMDb and TMDB portrait URLs use `t0-free-rpdb`.
5. With RPDB enabled and a custom key, generated URLs use the custom key.
6. Unsupported IDs, non-movie/series content, and non-portrait shapes keep their original artwork.
7. An RPDB load failure falls back to the original portrait.
8. The API key is stored per profile on the device and excluded from both the normal settings blob and provider credential sync; all other supported provider credentials continue to synchronize.
9. Focused common tests and the applicable Android compile/test tasks pass.
10. The signed GitHub release identifies RPDB support and its APK reports the new NuvioDV version and version code.
11. The RPDB integration row renders a bundled branded RPDB icon instead of the generic image glyph.
12. A repository-wide portrait-renderer audit has no compatible movie/series portrait path that bypasses RPDB solely because it uses a non-`MetaPreview` model.
13. Portrait-style Continue Watching items with compatible IMDb/TMDB identifiers select RPDB first and fall back to their original poster after a load failure.
14. Continue Watching full-background Card artwork and unsupported/non-media items retain their existing artwork selection.
15. Continue Watching Wide items preserve the original episode-thumbnail-first behavior when that preference is enabled; when a portrait poster is selected instead, compatible IMDb/TMDB identifiers may use RPDB with the original poster as fallback.
16. On Android, General > Integrations opens without an SVG-format exception and renders the branded RPDB icon from a native Android drawable.
17. A poster-cache episode thumbnail whose wrapper fails but whose encoded fallback is valid renders that fallback in every Continue Watching layout without replacing the episode thumbnail with a series poster.

## Staged Plan And Reconciliation Ledger

### Stage 1: Core settings and resolver

Status: `COMPLETE`

Requirements: `RPDB-2`, `RPDB-3`, `RPDB-4`, `RPDB-5`, `RPDB-9`

Acceptance evidence required:

- Focused tests prove effective-key and URL-resolution behavior.
- Android and iOS storage implementations compile.

Evidence:

- `RpdbPosterResolverTest` passes under `:composeApp:testAndroidHostTest`.
- Common and Android RPDB settings/storage sources compile in the same task.
- iOS execution is unavailable on Windows because the repository's native cinterop targets require macOS; the iOS actual follows the existing `NSUserDefaults` storage contract.

### Stage 2: Settings UI and credential integration

Status: `COMPLETE`

Requirements: `RPDB-1`, `RPDB-3`, `RPDB-7`, `RPDB-8`, `RPDB-9`

Acceptance evidence required:

- RPDB navigation and settings content compile for phone and tablet paths.
- Credential policy and provider snapshot tests cover RPDB.

Evidence:

- Android compilation covers both settings layouts and RPDB storage initialization.
- `ProviderCredentialModelsTest` and `ProfileSettingsCredentialPolicyTest` pass with RPDB cases.

### Stage 3: Global portrait application and fallback

Status: `COMPLETE`

Requirements: `RPDB-4`, `RPDB-5`, `RPDB-6`, `RPDB-8`, `RPDB-9`

Acceptance evidence required:

- Home, catalog, collection, library, and detail recommendation portrait paths use the shared resolver.
- RPDB load failure retains the source poster.
- Final focused tests and Android compilation pass.

Evidence:

- Home, catalog, collection, library, and detail recommendation portrait renderers use the shared RPDB resolver.
- Poster components retry with the source poster after an RPDB image load error.
- RPDB settings are collected as Compose state, so enable/key changes recompose visible portrait cards without an application restart.
- The focused RPDB, credential snapshot, and credential policy tests pass with Android main compilation.

### Final Reconciliation

Status: `COMPLETE`

Blockers: none.

Tracked deferrals: none.

### Stage 10: Continue Watching poster-cache fallback

Status: `COMPLETE`

Requirements: `RPDB-15`, `RPDB-17`

Objective:

- Keep episode thumbnails first while replacing an unusable poster-cache wrapper with the valid fallback URL already supplied by that wrapper.

Acceptance evidence required:

- A focused regression test reproduces the wrapper/fallback selection failure before the production change and passes afterward.
- Ordinary episode thumbnails and non-proxy artwork remain unchanged.
- Focused Continue Watching tests and Android compilation pass on the synchronized tree.

Blockers: none.

Tracked deferrals: none.

Verification evidence:

- `HomeContinueWatchingArtworkTest` reproduced the failure by selecting a `meta.remaxku.eu/poster-cache/` episode thumbnail whose encoded `fallback` was a valid TMDB image URL; before implementation the selector returned the failing wrapper.
- The shared Continue Watching candidate selector now unwraps only the known poster-cache host/path and only accepts HTTP(S) fallback values after the existing artwork-priority decision.
- The focused Home and RPDB Continue Watching test classes pass, covering episode-thumbnail priority, ordinary artwork, blur behavior, RPDB boundaries, and the poster-cache regression.
- Android main compilation completed as part of the focused host-test task, and `git diff --check` reports no whitespace errors.
- Reconciliation found that the blur predicate compared the resolved fallback URL with the unresolved wrapper; a second failing regression test was added, and the predicate now normalizes the thumbnail through the same resolver so unwatched-episode blur behavior is preserved.

### Stage 11: Local-only RPDB credential exception

Status: `COMPLETE`

Requirements: `RPDB-7`

Objective:

- Keep RPDB API keys in the existing profile-scoped device storage while removing RPDB from every provider-credential sync input, snapshot, and remote-apply path.

Acceptance evidence required:

- A focused regression test fails while provider snapshots still contain RPDB and passes after RPDB is excluded.
- Provider snapshots retain TMDB, MDBList, debrid, AnimeSkip, and IntroDB credentials.
- Provider sync no longer observes, loads, snapshots, or applies `RpdbSettingsRepository`, so a remote sync cannot clear a local RPDB key.
- The existing profile-settings credential policy still excludes the RPDB key.
- Focused credential tests and Android compilation pass.

Blockers: none.

Tracked deferrals: none.

Verification evidence:

- `ProviderCredentialModelsTest` failed before implementation because the snapshot contained `rpdb`, then passed after RPDB was removed from the snapshot contract.
- Provider snapshots still contain every configured debrid provider plus TMDB, MDBList, AnimeSkip, and IntroDB.
- `ProviderCredentialSync` no longer imports, observes, loads, snapshots, or applies `RpdbSettingsRepository`; unexpected remote RPDB rows are ignored because merges operate only on the local supported-provider snapshot.
- Android and iOS RPDB storage keep the API key under `ProfileScopedKey`, and profile changes still reload `RpdbSettingsRepository` through `ProfileRepository`.
- `ProfileSettingsCredentialPolicyTest` confirms the ordinary settings payload excludes `rpdb_api_key`; focused credential tests and Android compilation pass.

Verification:

- Requirements `RPDB-1` through `RPDB-17` are satisfied.
- `:composeApp:testAndroidHostTest` passes for the RPDB resolver, provider credential snapshot, and profile credential policy test classes.
- `:androidApp:assembleFullDebug` completes successfully.
- `git diff --check` reports no whitespace errors.
- GitHub Actions run `35361888866` built, verified, and published the signed ARM64 release successfully.
- Release `v0.4.23-nuviodv.5` targets source commit `77e722f5412ab0138559c5d9f394a65ea7b7910e`.
- The published APK independently reports package `com.darkaxt.nuviodv`, version `0.4.23-nuviodv.5`, version code `12218`, and ABI `arm64-v8a`.
- The published APK SHA-256 is `40bf5a731b571fb5181176989d5c7d1d439f9273f871b7d37dc2ed45083a5e17`, matching GitHub's release digest, and its DEX/resources contain the RPDB implementation.

### Stage 4: Release delivery

Status: `COMPLETE`

Requirements: `RPDB-10`

Acceptance evidence required:

- The verified source is committed and pushed to `cmp-rewrite`.
- The signed release workflow succeeds for the exact source commit.
- The published ARM64 APK reports version `0.4.23-nuviodv.5`, version code `12218`, package `com.darkaxt.nuviodv`, and contains the RPDB settings resources.

Release evidence:

- Workflow: `https://github.com/Darkaxt/NuvioMobile/actions/runs/35361888866`
- Release: `https://github.com/Darkaxt/NuvioMobile/releases/tag/v0.4.23-nuviodv.5`

Repository baseline note:

- The full `:composeApp:testAndroidHostTest` run reaches 1082 tests but has six failures in `AndroidDownloadLifecycleTest` and `DownloadSubtitlesTest`.
- The same six assertions fail when those classes are run against untouched commit `64858b48` in a separate worktree, so they are verified pre-existing failures unrelated to this change.

### Stage 5: Branded integration icon release

Status: `COMPLETE`

Requirements: `RPDB-11`

Acceptance evidence required:

- The RPDB integration row uses the shared cross-platform branded painter path on phone and tablet layouts.
- Android compilation packages the RPDB logo resource successfully.
- Signed release `v0.4.23-nuviodv.6` publishes package `com.darkaxt.nuviodv` with version code `12219`.

Release evidence:

- Workflow: `https://github.com/Darkaxt/NuvioMobile/actions/runs/35367593482`
- Release: `https://github.com/Darkaxt/NuvioMobile/releases/tag/v0.4.23-nuviodv.6`
- Source commit: `5de24225c9af0df412ab9ba2b59cd4c06bbefce7`
- Published APK SHA-256: `3f7e4d6ac67578bc3061556c6cdb1c1f44991b8512253e8dfa6d84c8ec91bd40`
- Independent inspection confirms package `com.darkaxt.nuviodv`, version `0.4.23-nuviodv.6`, version code `12219`, ARM64-only native libraries, and packaged `rpdb_logo.svg`.

### Stage 6: Portrait-path QA and gap remediation

Status: `COMPLETE`

Requirements: `RPDB-12`, `RPDB-13`, `RPDB-14`

Objective:

- Integrate the current upstream baseline before modifying portrait rendering.
- Inventory portrait-bearing production renderers and compare each compatible path with the shared RPDB contract.
- Add regression coverage before repairing every verified bypass.

Acceptance evidence required:

- The maintained branch contains the current upstream history without discarding NuvioDV behavior.
- A focused regression test fails against each verified bypass before production code changes and passes afterward.
- Compatible Continue Watching portrait items select RPDB with their original poster as fallback.
- Landscape, unsupported-ID, non-movie/series, episode-thumbnail, and cloud-library behavior remains unchanged.
- Focused RPDB/Continue Watching tests and the integrated Android debug build pass.
- A final repository-wide call-site audit finds no remaining compatible portrait bypass.

Evidence:

- The integrated merge tree contains upstream commit `90b58e2689e27c942ffb0b1d73f41d00c644195e` (`0.4.25`) while retaining the NuvioDV workflows, identity, version contract, and patched libmpv artifact.
- The production image-renderer audit identified three compatible Continue Watching portrait bypasses: the poster row, the action-sheet header, and the launch resume prompt. All now use one shared Continue Watching RPDB resolver and retry the original source artwork after an RPDB load failure.
- The renderer audit classified hero/backdrop, Card/Wide Continue Watching, episode, person/avatar, logo, folder-cover, cloud-library, and unsupported-ID images as intentionally outside the RPDB portrait contract; no compatible portrait bypass remains.
- Regression tests failed before implementation for the three missing call sites and the episode-thumbnail boundary, then passed after the shared resolver and fallbacks were integrated.
- Focused `RpdbPosterResolverTest`, `RpdbContinueWatchingArtworkTest`, `HomeContinueWatchingArtworkTest`, and `TraktIdUtilsTest` execution passes.
- The portrait-coverage, version-advance, upstream-sync workflow, and authenticated release-configuration contracts pass; the portrait-coverage check is now part of the daily upstream-sync verification.
- `:androidApp:assembleFullDebug` completes successfully after the final boundary fix.
- The resulting APK reports package `com.darkaxt.nuviodv`, label `NuvioDV`, version `0.4.25-nuviodv.1`, and version code `12222`.
- APK inspection finds one ARM64 `libmpv.so`; it is AArch64 and exports `dovi_parse_rpu`. The verified APK SHA-256 is `0dfcd43d32a017f0836b871d9b704bc434028cfe0e37f0035de88b0e7e2b4dac`.

Blockers: none.

Tracked deferrals: none.

### Stage 7: Continue Watching Wide portrait remediation

Status: `COMPLETE`

Requirements: `RPDB-15`

Objective:

- Repair the device-reproduced Wide layout bypass without changing the landscape Card renderer or unrelated Continue Watching behavior.

Acceptance evidence required:

- A focused regression check fails before production changes because the Wide portrait strip bypasses the shared RPDB resolver and lacks original-artwork fallback.
- Wide portrait artwork prefers the item's real poster, resolves it through RPDB, and retries the original poster after an RPDB image-load failure.
- If no poster artwork exists, existing episode-thumbnail fallback behavior remains available.
- The focused RPDB and Continue Watching checks pass.
- The integrated Android debug build passes.

Evidence:

- ADB inspection of tablet `R52W60CFTRL` running `0.4.25-nuviodv.1` reproduced the issue in the Wide layout and showed that RPDB-backed metadata was available at runtime.
- The Wide renderer was verified to use `continueWatchingArtworkUrl` directly while the Poster renderer alone used `rpdbPortraitSelection`; the regression check failed on this missing resolver/fallback contract before the production change.
- The Wide portrait strip now uses `continueWatchingPosterArtworkUrl`, `rpdbPortraitSelection`, and the original poster as its image-load fallback. The unchanged poster selector retains episode thumbnails only when no poster-like artwork exists.
- `.github/scripts/test_rpdb_portrait_coverage.py` passes with explicit Wide-layout coverage.
- Focused `RpdbContinueWatchingArtworkTest` and `HomeContinueWatchingArtworkTest` execution passes.
- `:androidApp:assembleFullDebug` completes successfully.
- `git diff --check` reports no whitespace errors.

Blockers: none.

Tracked deferrals: none.

### Stage 8: Restore Wide artwork priority

Status: `COMPLETE`

Requirements: corrected `RPDB-15`

Objective:

- Decouple RPDB fallback coverage from artwork selection and restore the pre-fix episode-thumbnail priority in the Wide layout.

Acceptance evidence required:

- A focused regression test fails against the current poster-first Wide selection before production changes.
- With episode thumbnails enabled, Wide selects the episode thumbnail before the series poster.
- With episode thumbnails disabled or absent, the existing poster and fallback chain remains intact.
- RPDB continues to replace compatible selected portrait posters and preserves their source fallback without replacing selected episode thumbnails.
- Focused Continue Watching/RPDB tests and the Android debug build pass.

Evidence:

- Before the production correction, `HomeContinueWatchingArtworkTest` failed to compile because the required Wide selector did not exist, and the portrait-coverage contract failed because Wide still called `continueWatchingPosterArtworkUrl`.
- `continueWatchingWideArtworkUrl` delegates to Nuvio's original artwork selector: enabled episode thumbnails take priority, while disabling them restores poster-first selection.
- The Wide renderer passes the selected artwork through `rpdbPortraitSelection`; its existing episode-thumbnail guard leaves selected thumbnails unchanged, while selected posters retain RPDB and original-poster fallback behavior.
- Focused `HomeContinueWatchingArtworkTest` and `RpdbContinueWatchingArtworkTest` execution passes.
- `.github/scripts/test_rpdb_portrait_coverage.py` passes and rejects a return to the poster-first Wide selector.
- `:androidApp:assembleFullDebug` completes successfully.

Blockers: none.

Tracked deferrals: none.

### Stage 9: Android Integrations crash regression

Status: `COMPLETE`

Requirements: `RPDB-1`, `RPDB-11`, `RPDB-16`

Objective:

- Remove the Android runtime dependency on decoding `rpdb_logo.svg` while preserving the branded icon and the existing iOS resource path.

Acceptance evidence required:

- A focused regression contract fails against the current SVG-backed Android painter before production changes and passes afterward.
- Android uses a native drawable resource for `IntegrationLogo.Rpdb`; iOS continues to use the shared SVG.
- Focused RPDB tests and the Android debug build pass.
- A signed normal release advances to `0.4.26-nuviodv.2` with version code `12227`.
- ADB reproduction on tablet `R52W60CFTRL` no longer emits `Android platform doesn't support SVG format` when the Integrations page is opened on the signed release.

Verification evidence:

- The regression contract failed before the Android painter change because `rpdb_logo.xml` was absent and Android still selected the Compose SVG resource; it passes after the native vector and painter change.
- Focused `RpdbPosterResolverTest` and `RpdbContinueWatchingArtworkTest` execution passes, and `:androidApp:assembleFullDebug` completed successfully before release publication.
- Release workflow run `35681508310` built, verified, and published the signed ARM64 APK successfully.
- GitHub release `v0.4.26-nuviodv.2` is a normal release (not draft or prerelease), targets `2f01213e2c7a39d37eddcbd9d51f673ed881e326`, and records SHA-256 `55ff95f8aba5d139340cb043583a2fed5cbeb87b21505c24f821802bb4439134` for the APK.
- Independent APK inspection confirms package `com.darkaxt.nuviodv`, version code `12227`, version name `0.4.26-nuviodv.2`, and signer certificate SHA-256 `1fb94424753a90f993c678b6fa4322579253bb303f22c335db395a9e2557d571`.
- `adb -s R52W60CFTRL install -r` completed successfully on the SM-X910 while preserving app data. Device package inspection reports version code `12227` and version name `0.4.26-nuviodv.2`.
- On the installed signed release, General > Integrations renders the RatingPosterDB row, the RatingPosterDB settings page opens with RPDB enabled, the app remains foregrounded, and the Android crash buffer remains empty.

Blockers: none.

Tracked deferrals: none.
