from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Group


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    amount = models.PositiveIntegerField(
        default=1000
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'Баланс пользователя {self.user.username}: {self.amount}'


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        unique_together = ('user', 'course')

    def __str__(self):
        return (
            f'Подписка пользователя {self.user.username} '
            f'на курс {self.course.title}'
        )


class StudentInGroup(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_in_groups'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='students_in_group'
    )

    def __str__(self):
        return f"{self.user} in {self.group}"