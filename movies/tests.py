import json

from django.test import TestCase
from django.urls import reverse

from .models import Contact, Genre, Director, Movie


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


class MovieCBVTest(TestCase):
	def setUp(self):
		self.genre = Genre.objects.create(name='TestGenre', description='d')
		self.director = Director.objects.create(name='TestDir', biography='b')
		self.movie = Movie.objects.create(title='Existing', release_year=2020, description='x', genre=self.genre)
		self.movie.directors.add(self.director)

	def test_movie_list_view(self):
		url = reverse('movies:movie_list')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, self.movie.title)

	def test_movie_create_view(self):
		url = reverse('movies:movie_create')
		data = {
			'title': 'New Movie',
			'release_year': 2025,
			'description': 'desc',
			'genre': self.genre.pk,
			'directors': [self.director.pk],
		}
		resp = self.client.post(url, data)
		# CreateView redirects to detail on success
		self.assertIn(resp.status_code, (302, 303))
		self.assertTrue(Movie.objects.filter(title='New Movie').exists())

	def test_movie_delete_view(self):
		# create a movie to delete
		m = Movie.objects.create(title='ToDel', release_year=2019, description='t', genre=self.genre)
		m.directors.add(self.director)
		url = reverse('movies:movie_delete', kwargs={'pk': m.pk})
		resp = self.client.post(url)
		# after delete view post, should redirect to list
		self.assertIn(resp.status_code, (302, 303))
		self.assertFalse(Movie.objects.filter(pk=m.pk).exists())

