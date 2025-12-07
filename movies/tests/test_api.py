import json

from django.test import TestCase
from django.urls import reverse

from ..models import Contact


class ContactAPITest(TestCase):
    def setUp(self):
        Contact.objects.create(name='Alice', email='alice@example.com', phone='123')

    def test_list_contacts(self):
        url = reverse('movies:contact_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_create_contact(self):
        url = reverse('movies:contact_api')
        payload = {'name': 'Bob', 'email': 'bob@example.com', 'phone': '555'}
        resp = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['name'], 'Bob')
        self.assertTrue(Contact.objects.filter(email='bob@example.com').exists())

    def test_delete_contact(self):
        c = Contact.objects.create(name='ToDelete', email='del@example.com', phone='000')
        url = reverse('movies:contact_detail_api', kwargs={'pk': c.pk})
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (200, 204))
        self.assertFalse(Contact.objects.filter(pk=c.pk).exists())
