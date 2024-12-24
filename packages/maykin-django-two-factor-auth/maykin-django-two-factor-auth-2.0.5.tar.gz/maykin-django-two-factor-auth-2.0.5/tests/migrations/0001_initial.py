# Generated by Django 2.2.2 on 2019-06-07 16:07

import tests.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    if settings.AUTH_USER_MODEL == "tests.User":
        operations = [
            migrations.CreateModel(
                name='User',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('password', models.CharField(max_length=128, verbose_name='password')),
                    ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                    ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                    ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                    ('is_staff', models.BooleanField(default=False)),
                    ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                    ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ],
                options={
                    'abstract': False,
                },
                managers=[
                    ('objects', tests.models.UserManager()),
                ],
            ),
        ]
    else:
        operations = []
