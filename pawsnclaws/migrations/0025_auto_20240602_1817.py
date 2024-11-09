# Generated by Django 5.0.3 on 2024-06-02 12:47

from django.db import migrations

def migrate_address_user(apps, schema_editor):
    Address = apps.get_model('pawsnclaws', 'Address')
    Register = apps.get_model('pawsnclaws', 'register')
    for address in Address.objects.all():
        try:
            user = Register.objects.get(username=address.user)
            address.user = user
            address.save()
        except Register.DoesNotExist:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', 'previous_migration_file'),
    ]

    operations = [
        migrations.RunPython(migrate_address_user),
    ]
class Migration(migrations.Migration):

    dependencies = [
        ('pawsnclaws', '0024_deliveryrequest_status'),
    ]

    operations = [
    ]
