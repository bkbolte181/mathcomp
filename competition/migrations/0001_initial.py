# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('first_name', models.CharField(help_text=b'First Name', max_length=100)),
                ('last_name', models.CharField(help_text=b'Last Name', max_length=100)),
                ('email', models.EmailField(help_text=b'Emory Email Address', unique=True, max_length=200, verbose_name=b'email address', error_messages={b'unique': b'A user with that email already exists.'})),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
