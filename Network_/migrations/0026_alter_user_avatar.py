# Generated by Django 4.2.5 on 2023-10-01 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Network_', '0025_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='image/default_avatar.png', upload_to='Network_/static/avatar'),
        ),
    ]
