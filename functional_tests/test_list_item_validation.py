from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys(Keys.ENTER)

        # The page refreshes and shows an error massage saying 
        # that list items cannot be empty
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(by='css selector', value='.has-error').text,
            "You can't have an empty list item"
        ))

        # She tries again with some text which now works
        self.get_input_box().send_keys('Buy milk')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')


        # Perversly, she now decides to enter another empty item
        self.get_input_box().send_keys(Keys.ENTER)

        # she recives a similar error massage
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(by='css selector', value='.has-error').text,
            "You can't have an empty list item"
        ))

        # And she can correct it by filling some text item.
        self.get_input_box().send_keys('Make tea')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
