# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-05-03 11:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0021_permits3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permit',
            name='areas',
        ),
        migrations.RemoveField(
            model_name='permit',
            name='subjects',
        ),
        migrations.DeleteModel(
            name='Permit',
        ),
        migrations.DeleteModel(
            name='PermitArea',
        ),
        migrations.DeleteModel(
            name='PermitSubject',
        ),
    ]