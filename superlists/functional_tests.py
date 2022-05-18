from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_list_and_retrive_it_later(self):
        # Edith has heard of a cool new online to-do list app. she 
        # goes to check it out 
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the tests')

        # She is invited to enter a to-do item straight away

        # She enters "Buy peacock feathers" into a box (Edith's 
        # hobby tying fly-fishing lures.)

        # When she hits enter the page updates, and now the page lists
        # "1: Buy peacock feathers" as a to-do list item

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again and now shows both items in the list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect

        # She visits that url and sees her list is still there

        # Satified she goes to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')