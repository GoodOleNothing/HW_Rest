from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsModerator, IsOwner
from materials.tasks import send_course_update_email


class SubscriptionAPIView(APIView): # Регистрация подписки
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        # Определяем права по действию
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Привязываем курс к текущему пользователю
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_email.delay(course.id)  # Запускаем асинхронную задачу


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = StandardResultsSetPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        # Привязываем урок к текущему пользователю
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator & IsOwner]
