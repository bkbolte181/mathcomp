# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_announcement_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200, verbose_name=b'email address')),
                ('identifier', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='email',
            field=models.EmailField(help_text=b'Email Address', unique=True, max_length=200, verbose_name=b'email address', error_messages={b'unique': b'A user with that email already exists.'}),
            preserve_default=True,
        ),
    ]
