# Generated by Django 5.0.3 on 2024-06-02 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawsnclaws', '0026_alter_address_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]
