from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase

from lists.views import index
from lists.models import Item

class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_can_save_POST_requests(self):
        response = self.client.post('/', data={'item_text':'new item text'})
        self.assertIn('new item text', response.content.decode())
        self.assertTemplateUsed(response, 'lists/index.html')


class ItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')