# Generated by Django 5.0.7 on 2024-11-15 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_videos', to='app.user'),
        ),
    ]
