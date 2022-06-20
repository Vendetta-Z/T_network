# Generated by Django 3.2.6 on 2022-06-11 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Network_', '0009_alter_userfollowing_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowing',
            name='following_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfollowing',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_to', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
