# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serv', '0002_remove_userdetailsmodel_org_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetailsmodel',
            name='org_name',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
