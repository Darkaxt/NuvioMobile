package com.nuvio.app.features.player

import android.app.Application
import android.content.Context
import com.nuvio.app.core.sync.decodeSyncBoolean
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import kotlin.test.BeforeTest
import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34], application = Application::class)
class PlayerPlaybackDetailsSettingsTest {
    @BeforeTest
    fun initialize() {
        val context = RuntimeEnvironment.getApplication()
        context.getSharedPreferences("nuvio_player_settings", Context.MODE_PRIVATE).edit().clear().commit()
        PlayerSettingsStorage.initialize(context)
        PlayerSettingsRepository.clearLocalState()
    }

    @Test
    fun `playback details default on and persist through profile sync`() {
        PlayerSettingsRepository.ensureLoaded()
        assertTrue(PlayerSettingsRepository.uiState.value.showPlaybackDetails)

        PlayerSettingsRepository.setShowPlaybackDetails(false)
        assertFalse(PlayerSettingsRepository.uiState.value.showPlaybackDetails)

        val payload = PlayerSettingsStorage.exportToSyncPayload()
        assertFalse(payload.decodeSyncBoolean("show_playback_details")!!)

        PlayerSettingsRepository.setShowPlaybackDetails(true)
        PlayerSettingsStorage.replaceFromSyncPayload(payload)
        PlayerSettingsRepository.onProfileChanged()
        assertFalse(PlayerSettingsRepository.uiState.value.showPlaybackDetails)
    }
}
