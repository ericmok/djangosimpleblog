# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20140926_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='edition',
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.RemoveField(
            model_name='post',
            name='reference_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='reference_type',
        ),
    ]
