# Generated by Django 4.2.5 on 2023-10-15 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Network_', '0028_alter_posts_postvidorimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='priview',
            field=models.ImageField(default='', upload_to='Network_/static/publication_image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='posts',
            name='PostVidOrImg',
            field=models.FileField(upload_to='Network_/static/publication_image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=["['jpeg', 'jpg', 'png']['mp4']"])]),
        ),
    ]
