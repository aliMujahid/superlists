import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, text):
        table = self.browser.find_element(by='id', value='id_table_list')
        rows = table.find_elements(by='tag name', value='tr')
        self.assertIn(text, [row.text for row in rows])        

    def test_can_create_list_and_retrive_it_later(self):
        # Edith has heard of a cool new online to-do list app. she 
        # goes to check it out 
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by='tag name', value='h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(by='id', value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 
                        'Enter a list item')

        # She enters "Buy peacock feathers" into a box (Edith's 
        # hobby tying fly-fishing lures.)
        inputbox.send_keys('Buy peacock feathers')
        
        # When she hits enter the page updates, and now the page lists
        # "1: Buy peacock feathers" as a to-do list item
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy peacock feathers')       

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element(by='id', value='id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and now shows both items in the list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')       

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect
        self.fail('finish the test')

        # She visits that url and sees her list is still there

        # Satified she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')