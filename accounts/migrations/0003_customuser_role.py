# Generated by Django 5.2 on 2025-04-11 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_password'),
        ('permissions', '0003_delete_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permissions.role'),
        ),
    ]
