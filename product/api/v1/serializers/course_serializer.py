from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import CustomUser


User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор студента."""

    email = serializers.CharField(
        source='user.email',
        read_only=True
    )
    first_name = serializers.CharField(
        source='user.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='user.last_name',
        read_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор группы."""
    students = StudentSerializer(
        many=True,
        source='students_in_group'
    )
    course = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True,
    )

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
            'students',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return obj.subscriptions.count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп."""
        total_capacity = sum(
            group.max_students
            for group in obj.groups.all()
        )
        return round(
            (obj.subscriptions.count() / total_capacity) * 100, 2
        ) if total_capacity else 0

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_users = CustomUser.objects.count()
        return (
            obj.subscriptions.count() / total_users
            ) * 100 if total_users else 0

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
