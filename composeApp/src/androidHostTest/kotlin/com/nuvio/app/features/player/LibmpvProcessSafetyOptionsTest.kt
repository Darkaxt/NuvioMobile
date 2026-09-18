package com.nuvio.app.features.player

import kotlin.test.Test
import kotlin.test.assertEquals

class LibmpvProcessSafetyOptionsTest {
    @Test
    fun disablesUnsupportedYtdlSubprocessResolution() {
        val options = linkedMapOf<String, String>()

        applyLibmpvProcessSafetyOptions { name, value ->
            options[name] = value
            0
        }

        assertEquals(mapOf("ytdl" to "no"), options)
    }
}
