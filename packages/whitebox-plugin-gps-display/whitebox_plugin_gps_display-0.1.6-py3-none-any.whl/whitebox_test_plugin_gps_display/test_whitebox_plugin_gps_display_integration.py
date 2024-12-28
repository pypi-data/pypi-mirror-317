from django.test import TestCase, Client
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from whitebox.routing import websocket_urlpatterns
from plugin.manager import plugin_manager


class TestWhiteboxPluginGpsDisplayIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        self.plugin = next(
            (
                x
                for x in plugin_manager.plugins
                if x.__class__.__name__ == "WhiteboxPluginGpsDisplay"
            ),
            None,
        )
        return super().setUp()

    def test_plugin_loaded(self):
        self.assertIsNotNone(self.plugin)

    def test_plugin_in_context(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "whitebox_plugin_gps_display/whitebox_plugin_gps_display.html",
            response.context["templates"],
        )
        self.assertIn(
            "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.css",
            response.context["css_files"],
        )
        self.assertIn(
            "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.js",
            response.context["js_files"],
        )

    def test_template_rendered(self):
        response = self.client.get(reverse("index"))
        self.assertContains(response, '<div id="whitebox-plugin-gps-display">')
        self.assertContains(response, '<div id="map">')

    async def test_websocket_gps_update(self):
        application = URLRouter(websocket_urlpatterns)
        communicator = WebsocketCommunicator(application, "/ws/flight/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to(
            {
                "type": "location_update",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "altitude": 100,
            }
        )

        # Check if the plugin receives the update
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "location_update")
        self.assertEqual(response["latitude"], 40.7128)
        self.assertEqual(response["longitude"], -74.0060)
        self.assertEqual(response["altitude"], 100)

        await communicator.disconnect()

    def test_plugin_embed_template(self):
        response = self.client.get(reverse("provider-map"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "whitebox_plugin_gps_display/map_only.html",
        )
        self.assertNotContains(
            response,
            '<div id="whitebox-plugin-gps-display">',
        )
        self.assertContains(
            response,
            '<div id="map" class="embedded">',
        )
