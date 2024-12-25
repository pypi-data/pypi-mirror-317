import asyncio

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from channels.routing import URLRouter
from django.urls import reverse
from aiohttp import web

from whitebox.routing import websocket_urlpatterns
from plugin.manager import plugin_manager
from whitebox.api import API


class TestWhiteboxPluginASDBGPSIntegration(TransactionTestCase):
    def setUp(self):
        plugin_manager.plugins = []
        plugin_manager.previously_discovered_plugins = {}
        plugin_manager.discover_plugins()

        self.plugin = next(
            (
                x
                for x in plugin_manager.plugins
                if x.__class__.__name__ == "WhiteboxPluginASDBGPS"
            ),
            None,
        )
        self.plugin.HOST = "127.0.0.1"
        self.plugin.PORT = "8090"
        self.application = URLRouter(websocket_urlpatterns)

        return super().setUp()

    def test_plugin_loaded(self):
        self.assertIsNotNone(self.plugin)

    def test_plugin_template_and_static_files(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "whitebox_plugin_adsb_gps/whitebox_plugin_adsb_gps.html",
            response.context["templates"],
        )
        self.assertIn(
            "/static/whitebox_plugin_adsb_gps/whitebox_plugin_adsb_gps.js",
            response.context["js_files"],
        )

    # async def test_websocket_flight_start_receives_data(self):
    #     communicator = WebsocketCommunicator(self.application, "/ws/flight/")
    #     connected, _ = await communicator.connect()
    #     self.assertTrue(connected)

    #     # Start flight
    #     await communicator.send_json_to({"type": "flight_start"})
    #     response = await communicator.receive_json_from()
    #     self.assertEqual(response["type"], "message")
    #     self.assertEqual(response["message"], "Flight started")

    #     # Wait for plugin to connect to mock Stratux
    #     await asyncio.sleep(2.0)

    #     # Check if plugin tasks are running
    #     self.assertTrue(self.plugin.is_active)
    #     self.assertIsNotNone(self.plugin.traffic_task)
    #     self.assertIsNotNone(self.plugin.situation_task)

    #     # Test location update
    #     response = await communicator.receive_json_from()
    #     self.assertEqual(response["type"], "location_update")
    #     self.assertEqual(response["latitude"], 0)
    #     self.assertEqual(response["longitude"], 0)
    #     self.assertEqual(response["altitude"], 0)

    #     await communicator.send_json_to({"type": "flight_end"})
    #     await communicator.disconnect()
