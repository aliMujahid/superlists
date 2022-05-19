from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase

from lists.views import index

class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')