# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20161229_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='pos',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
