from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class LessonSubscriptionTests(TestCase):

    def setUp(self):
        # Создаём пользователей
        self.user1 = User.objects.create_user(email='user1@test.com', password='pass1234')
        self.user2 = User.objects.create_user(email='user2@test.com', password='pass1234')

        # Создаём курсы
        self.course1 = Course.objects.create(title='Course 1', description='Desc 1', owner=self.user1)
        self.course2 = Course.objects.create(title='Course 2', description='Desc 2', owner=self.user2)

        # Создаём уроки
        self.lesson1 = Lesson.objects.create(title='Lesson 1', description='Lesson 1 desc', course=self.course1, owner=self.user1)
        self.lesson2 = Lesson.objects.create(title='Lesson 2', description='Lesson 2 desc', course=self.course2, owner=self.user2)

        # Настраиваем клиент
        self.client = APIClient()

    def test_lesson_list_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/materials/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что возвращаются уроки
        self.assertTrue(len(response.data['results']) > 0)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'title': 'New Lesson',
            'description': 'New description',
            'course': self.course1.id
        }
        response = self.client.post('/api/materials/lessons/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.filter(title='New Lesson').exists(), True)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated Lesson'}
        url = f'/api/materials/lessons/{self.lesson1.id}/update/'
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, 'Updated Lesson')

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = f'/api/materials/lessons/{self.lesson1.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson1.id).exists())

    def test_subscribe_course(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/materials/subscriptions/', {'course_id': self.course2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user1, course=self.course2).exists())
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_unsubscribe_course(self):
        # Создаём подписку вручную
        Subscription.objects.create(user=self.user1, course=self.course2)
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/materials/subscriptions/', {'course_id': self.course2.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.filter(user=self.user1, course=self.course2).exists())
        self.assertEqual(response.data['message'], 'Подписка удалена')

    def test_lesson_update_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Hack Lesson'}
        url = f'/api/materials/lessons/{self.lesson1.id}/update/'
        response = self.client.put(url, data)
        # Не владелец → 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)





