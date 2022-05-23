from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_create_list_and_retrive_it_later(self):
        # Edith has heard of a cool new online to-do list app. she 
        # goes to check it out 
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by='tag name', value='h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 
                        'Enter a to-do item')

        # She enters "Buy peacock feathers" into a box (Edith's 
        # hobby tying fly-fishing lures.)
        inputbox.send_keys('Buy peacock feathers')
        
        # When she hits enter the page updates, and now the page lists
        # "1: Buy peacock feathers" as a to-do list item
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Buy peacock feathers')       

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.get_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items in the list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')       

        # Satified she goes to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new list
        self.browser.get(self.live_server_url)
        inputbox = self.get_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        # She notices her list has a url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new visitor, Francis comes along 
        ## we use a new browser session to ensure that no information
        ## of Edith's is coming from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # Francis starts a new list by entering an item, he is
        # less intersting than Edith
        inputbox = self.get_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no sign of ediths list
        page_text = self.browser.find_element(by='tag name', value='body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
