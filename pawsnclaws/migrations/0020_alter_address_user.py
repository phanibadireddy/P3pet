# Generated by Django 5.0.3 on 2024-05-29 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pawsnclaws', '0019_alter_register_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]