import os
from datetime import datetime

from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.
from .services import Storage


class StorageTestCase(TestCase):
    def test_cd(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        storage = Storage(base_dir)

        storage.cd('Storage')
        self.assertEqual(storage.pwd, '/Storage')
        storage.cd('robeNaw')
        self.assertEqual(storage.pwd, '/Storage/robeNaw')
        storage.cd('/Storage')
        self.assertEqual(storage.pwd, '/Storage')
        storage.cd()
        self.assertEqual(storage.pwd, '/')
        storage.cd('Storage/robeNaw')
        self.assertEqual(storage.pwd, '/Storage/robeNaw')

    def test_get_dates(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        storage = Storage(base_dir)

        self.assertEqual(storage.get_dates(''),
                         (datetime.fromtimestamp(0), datetime.fromtimestamp(0), datetime.fromtimestamp(0)))
