import os
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 4

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by='id', value='id_list_table')
                rows = table.find_elements(by='tag name', value='tr')
                self.assertIn(text, [row.text for row in rows])        
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e