# Generated by Django 4.2.5 on 2023-10-11 19:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Network_', '0026_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='PostVidOrImg',
            field=models.FileField(default='', upload_to='Network_/static/publication_image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'jpeg', 'png'])]),
            preserve_default=False,
        ),
    ]