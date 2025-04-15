# Generated by Django 5.1.6 on 2025-04-03 15:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='completion_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='completed_lessons',
            field=models.ManyToManyField(blank=True, related_name='completed_by', to='courses.lesson'),
        ),
    ]
