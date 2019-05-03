# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-03 11:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0025_permits7'),
    ]

    operations = [
        migrations.AddField(
            model_name='permitseries',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='time created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='permitseries',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='time modified'),
        ),
    ]
