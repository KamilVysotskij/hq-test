# Generated by Django 4.2.10 on 2024-08-19 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_is_available_course_price_group_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='max_students',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
