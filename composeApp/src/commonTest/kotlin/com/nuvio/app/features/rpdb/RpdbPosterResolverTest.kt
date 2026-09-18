package com.nuvio.app.features.rpdb

import com.nuvio.app.features.home.PosterShape
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class RpdbPosterResolverTest {
    @Test
    fun `disabled integration keeps the source poster`() {
        val selection = RpdbPosterResolver.resolve(
            id = "tt0133093",
            type = "movie",
            posterShape = PosterShape.Poster,
            sourcePoster = "https://images.example/matrix.jpg",
            settings = RpdbSettings(enabled = false),
        )

        assertEquals("https://images.example/matrix.jpg", selection.primaryUrl)
        assertNull(selection.fallbackUrl)
    }

    @Test
    fun `blank custom key uses public tier zero key for imdb posters`() {
        val selection = RpdbPosterResolver.resolve(
            id = "tt0133093",
            type = "movie",
            posterShape = PosterShape.Poster,
            sourcePoster = "https://images.example/matrix.jpg",
            settings = RpdbSettings(enabled = true, apiKey = ""),
        )

        assertEquals(
            "https://api.ratingposterdb.com/t0-free-rpdb/imdb/poster-default/tt0133093.jpg",
            selection.primaryUrl,
        )
        assertEquals("https://images.example/matrix.jpg", selection.fallbackUrl)
    }

    @Test
    fun `custom key is used for tmdb series posters`() {
        val selection = RpdbPosterResolver.resolve(
            id = "tmdb:1399",
            type = "series",
            posterShape = PosterShape.Poster,
            sourcePoster = "https://images.example/game-of-thrones.jpg",
            settings = RpdbSettings(enabled = true, apiKey = "custom-key"),
        )

        assertEquals(
            "https://api.ratingposterdb.com/custom-key/tmdb/poster-default/series-1399.jpg",
            selection.primaryUrl,
        )
        assertEquals("https://images.example/game-of-thrones.jpg", selection.fallbackUrl)
    }

    @Test
    fun `landscape artwork and unsupported ids remain unchanged`() {
        val settings = RpdbSettings(enabled = true)

        val landscape = RpdbPosterResolver.resolve(
            id = "tt0133093",
            type = "movie",
            posterShape = PosterShape.Landscape,
            sourcePoster = "https://images.example/landscape.jpg",
            settings = settings,
        )
        val unsupported = RpdbPosterResolver.resolve(
            id = "kitsu:1",
            type = "series",
            posterShape = PosterShape.Poster,
            sourcePoster = "https://images.example/anime.jpg",
            settings = settings,
        )

        assertEquals("https://images.example/landscape.jpg", landscape.primaryUrl)
        assertNull(landscape.fallbackUrl)
        assertEquals("https://images.example/anime.jpg", unsupported.primaryUrl)
        assertNull(unsupported.fallbackUrl)
    }

    @Test
    fun `non movie or series content remains unchanged`() {
        val selection = RpdbPosterResolver.resolve(
            id = "tt0133093",
            type = "channel",
            posterShape = PosterShape.Poster,
            sourcePoster = "https://images.example/channel.jpg",
            settings = RpdbSettings(enabled = true),
        )

        assertEquals("https://images.example/channel.jpg", selection.primaryUrl)
        assertNull(selection.fallbackUrl)
    }
}
