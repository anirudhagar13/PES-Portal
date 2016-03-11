# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-04 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0005_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='branch',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='register',
            name='email',
            field=models.EmailField(default='abc@xyz.com', max_length=254),
        ),
        migrations.AddField(
            model_name='register',
            name='name',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='register',
            name='phone_no',
            field=models.IntegerField(default=1234567890),
        ),
        migrations.AddField(
            model_name='register',
            name='sem',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AddField(
            model_name='register',
            name='usn',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='event',
            name='no_part',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='register',
            name='event_id',
            field=models.IntegerField(null=True),
        ),
    ]
