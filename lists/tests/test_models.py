from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_items_are_asociated_with_lists(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.items.all())

        
    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla', list=list_)

        with self.assertRaises(ValidationError):
            item = Item(text='bla', list=list_)
            item.full_clean()

    def test_can_save_duplicate_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()

        Item.objects.create(text='bla', list=list1)
        item = Item(text='bla', list=list2)
        item.full_clean() #Should not raise
        
    def test_string_representation(self):
        item = Item(text='item text')
        self.assertEqual(str(item), 'item text')