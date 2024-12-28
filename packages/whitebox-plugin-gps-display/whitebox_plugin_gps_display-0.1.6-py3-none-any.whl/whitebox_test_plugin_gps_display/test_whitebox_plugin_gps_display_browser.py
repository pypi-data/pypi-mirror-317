import os
import logging

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import sync_playwright


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logging.getLogger("django.request").setLevel(logging.ERROR)
logging.getLogger("django.server").setLevel(logging.ERROR)


class TestWhiteboxPluginGpsDisplayBrowser(StaticLiveServerTestCase):
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

    def test_gps_display_loaded(self):
        div = self.page.query_selector("#whitebox-plugin-gps-display")
        self.assertIsNotNone(div)

    def test_map_loaded(self):
        div = self.page.query_selector("#map")
        self.assertIsNotNone(div)

    def test_leaflet_loaded(self):
        leaflet = self.page.query_selector(".leaflet-container")
        self.assertIsNotNone(leaflet)

    def test_css_applied(self):
        map_element = self.page.wait_for_selector("#map")
        map_height = map_element.evaluate(
            "(element) => window.getComputedStyle(element).height"
        )
        self.assertEqual(map_height, "400px")

    def test_gps_update_reflected_on_map(self):
        self.page.wait_for_selector(".leaflet-container")
        self.page.evaluate("window.updateGPSLocation(51.5074, -0.1278);")
        map_center = self.page.evaluate("map.getCenter();")
        self.assertEqual(map_center["lat"], 51.5074)
        self.assertEqual(map_center["lng"], -0.1278)
