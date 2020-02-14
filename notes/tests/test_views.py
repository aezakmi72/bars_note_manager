import json
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Note, Category
from ..serializers import NoteSerializer, CategorySerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import status


client = Client()


class GetAllCats(TestCase):
    def setUp(self):
        Category.objects.create(title='purchases', slug='purchases')
        Category.objects.create(title='ideas', slug='ideas')
        Category.objects.create(title='garbage', slug='garbage')

    def test_get_all_cats(self):
        response = client.get(reverse('notes:categories'))
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, JsonResponse(
            serializer.data, safe=False).content)


class GetAllNotes(TestCase):
    def setUp(self):
        self.Ivan = User.objects.create_user(
            username='Ivan', password='qwerty')
        Note.objects.create(title='123', context='456',
                            bookmark=True, creator=self.Ivan)
        Note.objects.create(title='123', context='Lorem ipsum',
                            creator=self.Ivan)
        Note.objects.create(title='123', context='213', creator=self.Ivan)
        Note.objects.create(title='321', context='421',
                            creator=self.Ivan)

    def test_get_all_notes_anon(self):
        response = client.get(reverse('notes:note_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_notes(self):
        client.login(username='Ivan', password='qwerty')
        response = client.get(reverse('notes:note_list'))
        notes = Note.objects.filter(creator=self.Ivan)
        serializer = NoteSerializer(notes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleNote(TestCase):
    def setUp(self):
        self.Ivan = User.objects.create_user(
            username='Ivan', password='qwerty')
        self.book = Note.objects.create(
            title='book', context='456', creator=self.Ivan)
        self.milk = Note.objects.create(
            title='milk', context='muu', creator=self.Ivan)

    def test_get_single_note(self):
        client.login(username='Ivan', password='qwerty')
        response = client.get(
            reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}))
        book = Note.objects.get(pk=self.book.pk)
        serializer = NoteSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, JsonResponse(
            serializer.data, safe=False).content)

    def test_get_nonex_note(self):
        response = client.get(
            reverse('notes:api_note_detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_note_anon(self):
        response = client.get(
            reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateNote(TestCase):
    def setUp(self):
        self.Ivan = User.objects.create_user(
            username='Ivan', password='qwerty')
        client.login(username='Ivan', password='qwerty')
        self.invalid_data = {
            'title': '000'
        }
        self.valid_data = {
            'title': '123',
            'context': '345'
        }

    def test_create_valid_data(self):
        response = client.post(reverse('notes:create_note'), data=json.dumps(
            self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_data(self):
        response = client.post(reverse('notes:create_note'), data=json.dumps(
            self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteNote(TestCase):
    def setUp(self):
        self.Ivan = User.objects.create_user(
            username='Ivan', password='qwerty')        
        self.book = Note.objects.create(
            title='book', context='456', creator=self.Ivan)          

    def test_delete_note(self):
        client.login(username='Ivan', password='qwerty')
        response = client.delete(reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    def test_delete_note_anon(self):        
        response = client.delete(reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UpdateNote(TestCase):
    def setUp(self):
        self.Ivan = User.objects.create_user(
            username='Ivan', password='qwerty')
        client.login(username='Ivan', password='qwerty')
        self.book = Note.objects.create(
            title='book', context='456', creator=self.Ivan)
        self.invalid_data = {
            'title': '000'
        }
        self.valid_data = {
            'title': '123',
            'context': '345'
        }

    def test_update_note_valid_data(self):
        response = client.put(reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}), data=json.dumps(
            self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_note_invalid_data(self):
        response = client.put(reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}), data=json.dumps(
            self.invalid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonex_note(self):
        response = client.put(reverse('notes:api_note_detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'}), data=json.dumps(
            self.valid_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_note_anon(self):
        client.logout()
        response = client.get(
            reverse('notes:api_note_detail', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
