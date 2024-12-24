# coding: utf-8
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gisdo', '0007_auto_20200207_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdounit',
            name='unit',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='gisdo',
                to='unit.Unit',
                verbose_name='Организация'),
        ),
    ]
