import os
import logging
import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logging.getLogger("django.request").setLevel(logging.ERROR)
logging.getLogger("django.server").setLevel(logging.ERROR)

TEST_TRAFFIC_DATA = {
    "Icao_addr": 8393736,
    "Reg": "",
    "Tail": "AIC2605",
    "Emitter_category": 3,
    "SurfaceVehicleType": 0,
    "OnGround": False,
    "Addr_type": 0,
    "TargetType": 1,
    "SignalLevel": -28.67420152340263,
    "SignalLevelHist": [
        -29.710222947912218,
        -30.931264652779298,
        -33.458234581220395,
        -31.70053304058364,
        -32.14670164989233,
        -33.47753658996677,
        -28.67420152340263,
        -33.19664486585437,
    ],
    "Squawk": 242,
    "Position_valid": True,
    "Lat": 19.38235,
    "Lng": 72.75217,
    "Alt": 11275,
    "GnssDiffFromBaroAlt": 250,
    "AltIsGNSS": False,
    "NIC": 8,
    "NACp": 9,
    "Track": 8,
    "TurnRate": 0,
    "Speed": 345,
    "Speed_valid": True,
    "Vvel": 1984,
    "Timestamp": "2024-12-22T09:16:12.573Z",
    "PriorityStatus": 0,
    "Age": 0.39,
    "AgeLastAlt": 0.39,
    "Last_seen": "0001-01-01T00:13:17.7Z",
    "Last_alt": "0001-01-01T00:13:17.7Z",
    "Last_GnssDiff": "0001-01-01T00:13:17.7Z",
    "Last_GnssDiffAlt": 11275,
    "Last_speed": "0001-01-01T00:13:16.07Z",
    "Last_source": 1,
    "ExtrapolatedPosition": False,
    "Last_extrapolation": "0001-01-01T00:13:16.44Z",
    "AgeExtrapolation": 0.56,
    "Lat_fix": 19.370852,
    "Lng_fix": 72.75042,
    "Alt_fix": 11075,
    "BearingDist_valid": True,
    "Bearing": 250.832328119001,
    "Distance": 8268.217811843375,
    "DistanceEstimated": 13295.535248127946,
    "DistanceEstimatedLastTs": "2024-12-22T09:16:12.573Z",
    "ReceivedMsgs": 490,
    "IsStratux": False,
}
TEST_TRAFFIC_DATA_JSON = json.dumps(TEST_TRAFFIC_DATA)


class TestWhiteboxPluginASDBGPSBrowser(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        self.page.goto(f"{self.live_server_url}{reverse('index')}")

    def test_gps_simulator_loaded(self):
        div = self.page.query_selector("#whitebox-plugin-adsb-gps")
        self.assertIsNotNone(div)

    def test_update_current_location(self):
        self.page.wait_for_selector("#whitebox-plugin-adsb-gps")

        function_exists = self.page.evaluate(
            "typeof window.updateCurrentLocation === 'function'"
        )
        self.assertTrue(function_exists)

        self.page.evaluate("window.updateCurrentLocation(1.1, 2.2, 3.3, 0);")

        latitude = self.page.query_selector("#gps-data-latitude").inner_text()
        longitude = self.page.query_selector("#gps-data-longitude").inner_text()
        altitude = self.page.query_selector("#gps-data-altitude").inner_text()
        gps_timestamp = self.page.query_selector("#gps-data-timestamp").inner_text()

        self.assertEqual(latitude, "1.1")
        self.assertEqual(longitude, "2.2")
        self.assertEqual(altitude, "3.3")
        self.assertEqual(gps_timestamp, "0")

    def test_update_traffic_data(self):
        self.page.wait_for_selector("#whitebox-plugin-adsb-gps")

        function_exists = self.page.evaluate(
            "typeof window.updateTrafficData === 'function'"
        )
        self.assertTrue(function_exists)

        self.page.evaluate(f"window.updateTrafficData({TEST_TRAFFIC_DATA_JSON});")

        self.page.wait_for_selector(f"tr[data-icao='{TEST_TRAFFIC_DATA['Icao_addr']}']")

        traffic_row = self.page.query_selector(
            f"tr[data-icao='{TEST_TRAFFIC_DATA['Icao_addr']}']"
        )
        self.assertIsNotNone(traffic_row)

        callsign = traffic_row.query_selector("td:nth-child(1)").inner_text()
        code = traffic_row.query_selector("td:nth-child(2)").inner_text()
        location = traffic_row.query_selector("td:nth-child(3)").inner_text()
        altitude = traffic_row.query_selector("td:nth-child(4)").inner_text()
        speed = traffic_row.query_selector("td:nth-child(5)").inner_text()
        course = traffic_row.query_selector("td:nth-child(6)").inner_text()
        power = traffic_row.query_selector("td:nth-child(7)").inner_text()
        age = traffic_row.query_selector("td:nth-child(8)").inner_text()

        self.assertEqual(callsign, TEST_TRAFFIC_DATA["Tail"])
        self.assertEqual(code, str(TEST_TRAFFIC_DATA["Icao_addr"]))
        self.assertEqual(location, "19° 23' N 72° 45' E")
        self.assertEqual(altitude, "11,275")
        self.assertEqual(speed, "345")
        self.assertEqual(course, "8°")
        self.assertEqual(power, "-28.67")
        self.assertEqual(age, "0.4")
