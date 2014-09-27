# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20140926_2033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='edition',
            options={'ordering': ['modified_at']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['modified_at']},
        ),
        migrations.AddField(
            model_name='edition',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 9, 26), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edition',
            name='modified_at',
            field=models.DateTimeField(default=datetime.date(2014, 9, 26), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=django.utils.datetime_safe.date.today, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 26, 21, 6, 46, 197275), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='edition',
            name='post',
            field=models.ForeignKey(to='blogs.Post', related_name='editions'),
        ),
    ]
