# coding: utf-8
from __future__ import unicode_literals

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0016_auto_20190820_1140'),
        ('gisdo', '0004_delete_plugin_work_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='gisdounit',
            name='related_to_mo',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='unit.Unit',
                verbose_name='Относится к МО'),
        ),
    ]
