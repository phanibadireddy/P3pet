# Generated by Django 5.0.3 on 2024-06-09 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawsnclaws', '0031_ads_owusername_purchase_payment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(max_length=10)),
                ('complaintname', models.CharField(max_length=20)),
                ('complaintdesc', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pawsnclaws.register')),
            ],
        ),
    ]