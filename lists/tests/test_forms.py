from django.test import TestCase

from lists.models import List, Item
from lists.forms import (ItemForm, EMPTY_ITEM_ERROR,
                        DUPLICATE_ITEM_ERROR,
                        ExistingListItemForm
                        )

class ItemFormsTest(TestCase):
    def test_form_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_method_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text':'new item'})
        new_item = form.save(for_list=list_)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'new item')
        self.assertEqual(new_item.list, list_)


class ExistinListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_list_item(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins')
        form = ExistingListItemForm(for_list=list_, data={'text':'no twins'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])