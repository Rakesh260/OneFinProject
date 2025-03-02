from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from movie_collection.factories import UserFactory, CollectionFactory
from movie_collection.models import Collection


class RegisterUserViewTests(APITestCase):

    def test_successful_user_registration(self):
        """
        Test that a user can be registered successfully and an access token is returned.
        """
        url = reverse('register-user')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')

        print('registaration', response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('access_token', response.data)

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_data(self):
        """
        Test that the API returns a 400 Bad Request response when invalid data is provided.
        """
        url = reverse('register-user')
        data = {
            'username': '',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('username', response.data)


class MovieListViewTests(APITestCase):

    def test_get_all_movies(self):
        """
        Test to get all movies from the API
        """

        url = reverse('fetch-all-movies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)
        self.assertEqual(response.data['result'], 'success')


class UserMovieCollectionTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_user_collection(self):
        """
        Test fetching all collections for the authenticated user.
        """
        url = reverse('user-movie-collection')
        CollectionFactory.create(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_post_new_collection(self):
        """
        Test to post new collection with all values
        """
        url = reverse('user-movie-collection')
        data = {
            "title": "Top Comedy Movies",
            "description": "A collection of the funniest movies to make you laugh.",
            "movies": [
                {
                    "title": "The Hangover",
                    "description": "Three friends lose their groom-to-be in Las Vegas and must retrace their steps to "
                                   "find him.",
                    "genres": "Comedy, Adventure",
                    "uuid": "111e4567-e89b-12d3-a456-426614174001"
                },
                {
                    "title": "Dumb and Dumber",
                    "description": "Two dumb friends go on a road trip to return a lost briefcase.",
                    "genres": "Comedy",
                    "uuid": "222e4567-e89b-12d3-a456-426614174002"
                },
                {
                    "title": "Superbad",
                    "description": "Two high school friends attempt to buy alcohol for a party.",
                    "genres": "Comedy, Teen",
                    "uuid": "333e4567-e89b-12d3-a456-426614174003"
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)
        self.assertTrue(Collection.objects.filter(uuid=response.data['collection_uuid']).exists())

    def test_post_new_collection_invalid_data(self):
        """
        Test creating a new collection with invalid data.
        """
        url = reverse('user-movie-collection')
        invalid_data = {
            "title": "",
            "description": "A collection with no title.",
            "movies": []
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('result', response.data)


class CollectionDetailView(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.collection = CollectionFactory(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_collection_detail(self):
        """
        Test to get collection by uuid
        """
        url = reverse('collection-detail', args=[self.collection.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)
        self.assertIn('movies', response.data)

    def test_get_collection_not_found(self):
        """
        Test fetching a non-existent collection.
        """
        url = reverse('collection-detail', args=['bbbfe607-b18a-4699-bed7-8690648dd6d9'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

    def test_update_collection(self):
        """
        Test to update a collection
        """
        url = reverse('collection-detail', args=[self.collection.uuid])
        data = {
            'title': 'Updated Collection',
            'description': 'Updated description.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_update_collection_not_found(self):
        """
        Test updating a non-existent collection.
        """
        url = reverse('collection-detail', args=['bbbfe607-b18a-4699-bed7-8690648dd6d9'])
        data = {
            'title': 'Updated Collection',
            'description': 'Updated description.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)

    def test_delete_collection(self):
        """
        Test to delete a collection.
        """
        url = reverse('collection-detail', args=[self.collection.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_collection_not_found(self):
        """
        Test deleting a non-existent collection.
        """
        url = reverse('collection-detail', args=['bbbfe607-b18a-4699-bed7-8690648dd6d9'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.data)
