from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits enter on the empty input box

        # The page refreshes and shows an error massage saying 
        # that list items cannot be empty

        # She tries again with some text which now works

        # Perversly, she now decides to enter another empty item

        # she recives a similar error massage

        # And she can correct it by filling some text item.
        self.fail('write me')