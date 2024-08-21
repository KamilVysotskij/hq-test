from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription, StudentInGroup


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """

    if created:
        course = instance.course  # Get the course the user just subscribed to
        group = course.groups.annotate(
            student_count=Count('students_in_group__user')
            ).order_by('student_count', 'id').first()
        if group.student_count < group.max_students:
            StudentInGroup.objects.create(user=instance.user, group=group)
        # Adds the user to the selected group
        else:
            raise ValidationError('All groups are filled')
