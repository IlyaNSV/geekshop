# Generated by Django 2.2 on 2020-07-21 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20200717_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='теги')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='о себе')),
                ('gender', models.CharField(choices=[('мужской', 'M'), ('женский', 'W')], default='мужской', max_length=1, verbose_name='пол')),
            ],
        ),
    ]