#!/usr/bin/env python3

from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on an empty box

        # The home page refreshes, and there is an error message saying 
        # that list items cannot be blank

        # She tries again with some text for the item, which now works
        self.fail("write me")