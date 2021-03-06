#!/usr/bin/env python3

from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import List, Item 


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        list_ = List()
        list_.save()
        first_item.list = list_
        first_item.text = "The first (ever) list item"
        first_item.save()
        self.assertEqual(first_item.list, list_)

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()
        self.assertEqual(second_item.list, list_)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertQuerysetEqual(
            Item.objects.all(),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")

    def test_cannot_save_empty_list_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text="bla", list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text="bla", list=list_)
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean()   # should not raise

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")