from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase

from lists.views import index
from lists.models import Item

class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')


class ViewListTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):
    def test_can_save_POST_requests(self):
        response = self.client.post('/lists/new', data={'item_text':'new item text'})
        
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'new item text')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text':'new item text'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


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