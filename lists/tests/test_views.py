from django.utils.html import escape
from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

class IndexTest(TestCase):
    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_index_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class ViewListTest(TestCase):
    def post_invalid_item(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/', 
            data={'text':''}
        )

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(list_.get_absolute_url())
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_can_save_POST_request_to_and_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
        f'/lists/{correct_list.id}/',
        data={'text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_view_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
        f'/lists/{correct_list.id}/',
        data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_item()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_item()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_item()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_list_validation_errors_shown_on_page(self):
        response = self.post_invalid_item()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))



class NewListTest(TestCase):
    def test_can_save_POST_requests(self):
        response = self.client.post('/lists/new', data={'text':'new item text'})
        
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'new item text')

    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'text':'new item text'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_render_index_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')

    def test_invaild_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_are_not_saved(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
