# Generated by Django 4.2.5 on 2023-10-10 10:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videosPost', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video_post',
            old_name='posted_in',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='video_post',
            name='video',
            field=models.FileField(upload_to='videoposts/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]
