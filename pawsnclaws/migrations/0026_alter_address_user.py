# Generated by Django 5.0.3 on 2024-06-02 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawsnclaws', '0025_auto_20240602_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pawsnclaws.register'),
        ),
    ]
