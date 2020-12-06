from django.test import TestCase
import unittest
from django.test import Client

c = Client()

class PropertyMainListTestCase(TestCase):
    def property_main_list_filter_success_facility(self):
        response = c.get("property?facility=1")
        self.assertEqual(response.status_code,200)

class PropertyMainListTestCase(TestCase):
    def property_main_list_filter_success_(self):
        response = c.get("property?host=True&type=집 전체&facility=1&category=통나무집&rule=흡연 금지&review=True&facility=식기류")
        self.assertEqual(response.status_code,200)



