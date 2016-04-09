# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0007_auto_20160404_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usn', models.CharField(max_length=10)),
                ('event_id', models.IntegerField()),
                ('comment', models.CharField(max_length=100000000000000)),
                ('creat_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='comments',
            unique_together=set([('usn', 'creat_date')]),
        ),
    ]
