# Generated by Django 5.2 on 2025-04-11 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0002_alter_userrole_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
