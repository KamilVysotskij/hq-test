# Generated by Django 4.2.10 on 2024-08-18 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_is_available_course_price_group_course_and_more'),
        ('users', '0002_balance_amount_balance_user_subscription_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='courses.group'),
            preserve_default=False,
        ),
    ]
