# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0003_remove_pending_transactions_book_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pending_transactions',
            name='book_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='pending_transactions',
            unique_together=set([('buyer_id', 'seller', 'book_name')]),
        ),
    ]
