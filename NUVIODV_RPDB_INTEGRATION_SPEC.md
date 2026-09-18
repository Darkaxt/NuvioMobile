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
- `RPDB-7`: Keep the custom API key profile-scoped and out of ordinary profile-settings payloads. Include it in the existing provider-credential synchronization path.
- `RPDB-8`: Changing RPDB settings must take effect when returning to portrait-bearing screens without requiring an application restart.
- `RPDB-9`: Cover the resolver, settings policy, and credential handling with focused tests.
- `RPDB-10`: Publish the verified integration as a signed NuvioDV Android release with a version newer than the installed test build.

## Acceptance Criteria

1. General > Integrations contains an RPDB entry on phone and tablet layouts.
2. The RPDB page exposes an enable switch and optional masked custom-key field, and explains the public fallback.
3. With RPDB disabled, existing portrait URLs are unchanged.
4. With RPDB enabled and no custom key, IMDb and TMDB portrait URLs use `t0-free-rpdb`.
5. With RPDB enabled and a custom key, generated URLs use the custom key.
6. Unsupported IDs, non-movie/series content, and non-portrait shapes keep their original artwork.
7. An RPDB load failure falls back to the original portrait.
8. The API key is excluded from the normal settings blob and included in provider credential sync.
9. Focused common tests and the applicable Android compile/test tasks pass.
10. The signed GitHub release identifies RPDB support and its APK reports the new NuvioDV version and version code.

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

Verification:

- All ten requirements and all ten acceptance criteria are satisfied.
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
