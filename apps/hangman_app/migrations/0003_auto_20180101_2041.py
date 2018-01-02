# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 04:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hangman_app', '0002_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_by', to='hangman_app.User'),
        ),
    ]
