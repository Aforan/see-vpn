# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 03:06
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('serv', '0003_userdetailsmodel_org_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetailsmodel',
            name='contact_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
    ]
