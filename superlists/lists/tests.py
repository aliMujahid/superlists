from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase

from lists.views import index

class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_can_save_POST_requests(self):
        response = self.client.post('/', data={'item_text':'new item text'})
        self.assertIn('new item text', response.content.decode())
        self.assertTemplateUsed(response, 'lists/index.html')