package com.nuvio.app.features.collection

import android.app.Application
import android.content.Context
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.nuvio.app.core.ui.NuvioTheme
import com.nuvio.app.features.home.HomeCatalogSettingsRepository
import com.nuvio.app.features.home.HomeCatalogSettingsStorage
import org.junit.Rule
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import kotlin.test.AfterTest
import kotlin.test.BeforeTest
import kotlin.test.Test

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34], application = Application::class)
class CollectionManagementScreenTest {
    @get:Rule
    val compose = createComposeRule()

    @BeforeTest
    fun initialize() {
        val context = RuntimeEnvironment.getApplication()
        context.getSharedPreferences("nuvio_collections", Context.MODE_PRIVATE).edit().clear().commit()
        context.getSharedPreferences("nuvio_home_catalog_settings", Context.MODE_PRIVATE).edit().clear().commit()
        CollectionStorage.initialize(context)
        HomeCatalogSettingsStorage.initialize(context)
        CollectionRepository.clearLocalState()
        HomeCatalogSettingsRepository.clearLocalState()
    }

    @AfterTest
    fun clearState() {
        CollectionRepository.clearLocalState()
        HomeCatalogSettingsRepository.clearLocalState()
    }

    @Test
    fun rebuildingHomeLayoutShowsSuccessConfirmation() {
        compose.setContent {
            NuvioTheme {
                CollectionManagementScreen(
                    onBack = {},
                    onNavigateToEditor = {},
                )
            }
        }

        compose.onNodeWithContentDescription("Rebuild Home Layout").performClick()

        compose.onNodeWithText("Home Layout Refreshed").assertIsDisplayed()
        compose.onNodeWithText(
            "The Home Layout collection rows now match your current Collections order.",
        ).assertIsDisplayed()
        compose.onNodeWithText("OK").performClick()
        compose.onNodeWithText("Home Layout Refreshed").assertDoesNotExist()
    }
}
