# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_siteuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='created_at',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=True,
        ),
    ]
