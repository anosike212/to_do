from django.test import TestCase
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