# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('reference_type', models.CharField(blank=True, default=None, max_length=16, choices=[('Edition', 'Edition'), ('Quote', 'Quote')], null=True)),
                ('reference_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('order', models.IntegerField()),
                ('edition', models.ForeignKey(to='blogs.Edition')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blogs.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edition',
            name='post',
            field=models.ForeignKey(to='blogs.Post'),
            preserve_default=True,
        ),
    ]
