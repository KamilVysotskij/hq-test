from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all().prefetch_related(
            'students_in_group__user'
        )


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        user = request.user
        course = self.get_object()
        if Subscription.objects.filter(user=user, course=course).exists():
            return Response(
                data={'error': 'Вы уже подписаны на этот курс'},
                status=status.HTTP_400_BAD_REQUEST
            )
        balance = user.balance
        if balance.amount < course.price:
            return Response(
                data={'error': 'Недостаточно средств на балансе'},
                status=status.HTTP_400_BAD_REQUEST
            )
        balance.amount -= course.price
        balance.save()
        subscription = Subscription.objects.create(user=user, course=course)
        return Response(
            data={
                'message': 'Подписка оформлена',
                'subscription': subscription.id
            },
            status=status.HTTP_201_CREATED
        )


class AvailableCoursesViewSet(viewsets.ModelViewSet):
    """Список доступных для покупки курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Получение списка доступных курсов для пользователя."""
        user = self.request.user
        return Course.objects.filter(
            is_available=True
        ).exclude(
            subscriptions__user=user
        )


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet для подписок."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Получение списка подписок для авторизованного пользователя."""
        return Subscription.objects.filter(user=self.request.user)