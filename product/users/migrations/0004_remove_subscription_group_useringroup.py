# Generated by Django 4.2.10 on 2024-08-19 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_is_available_course_price_group_course_and_more'),
        ('users', '0003_subscription_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='group',
        ),
        migrations.CreateModel(
            name='UserInGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
