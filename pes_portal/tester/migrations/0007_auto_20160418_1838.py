# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0006_auto_20160416_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='book_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='seller',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
