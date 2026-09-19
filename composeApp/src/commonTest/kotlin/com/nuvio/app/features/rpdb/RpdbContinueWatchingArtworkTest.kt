package com.nuvio.app.features.rpdb

import com.nuvio.app.features.watchprogress.ContinueWatchingItem
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class RpdbContinueWatchingArtworkTest {
    @Test
    fun `continue watching imdb portrait selects rpdb and preserves source fallback`() {
        val selection = item(id = "tt0903747", type = "series")
            .resolveRpdbPortraitSelection(
                sourcePoster = "https://images.example/breaking-bad.jpg",
                settings = RpdbSettings(enabled = true),
            )

        assertEquals(
            "https://api.ratingposterdb.com/t0-free-rpdb/imdb/poster-default/tt0903747.jpg",
            selection.primaryUrl,
        )
        assertEquals("https://images.example/breaking-bad.jpg", selection.fallbackUrl)
    }

    @Test
    fun `continue watching tmdb series portrait uses series endpoint`() {
        val selection = item(id = "tmdb:1396", type = "series")
            .resolveRpdbPortraitSelection(
                sourcePoster = "source.jpg",
                settings = RpdbSettings(enabled = true, apiKey = "personal-key"),
            )

        assertEquals(
            "https://api.ratingposterdb.com/personal-key/tmdb/poster-default/series-1396.jpg",
            selection.primaryUrl,
        )
        assertEquals("source.jpg", selection.fallbackUrl)
    }

    @Test
    fun `continue watching unsupported trakt id keeps source portrait`() {
        val selection = item(id = "trakt:1388", type = "series")
            .resolveRpdbPortraitSelection(
                sourcePoster = "source.jpg",
                settings = RpdbSettings(enabled = true),
            )

        assertEquals("source.jpg", selection.primaryUrl)
        assertNull(selection.fallbackUrl)
    }

    @Test
    fun `continue watching episode thumbnail remains unchanged`() {
        val item = item(id = "tt0903747", type = "series").copy(
            imageUrl = "episode.jpg",
            poster = null,
            episodeThumbnail = "episode.jpg",
        )

        val selection = item.resolveRpdbPortraitSelection(
            sourcePoster = "episode.jpg",
            settings = RpdbSettings(enabled = true),
        )

        assertEquals("episode.jpg", selection.primaryUrl)
        assertNull(selection.fallbackUrl)
    }

    @Test
    fun `continue watching cloud library item remains unchanged`() {
        val selection = item(id = "cloud:item", type = "cloud")
            .resolveRpdbPortraitSelection(
                sourcePoster = "cloud.jpg",
                settings = RpdbSettings(enabled = true),
            )

        assertEquals("cloud.jpg", selection.primaryUrl)
        assertNull(selection.fallbackUrl)
    }

    private fun item(id: String, type: String) = ContinueWatchingItem(
        parentMetaId = id,
        parentMetaType = type,
        videoId = id,
        title = "Title",
        subtitle = "",
        imageUrl = "source.jpg",
        poster = "source.jpg",
        resumePositionMs = 1L,
        durationMs = 2L,
        progressFraction = 0.5f,
    )
}
