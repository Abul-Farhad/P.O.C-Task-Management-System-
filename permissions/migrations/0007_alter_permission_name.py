# Generated by Django 5.2 on 2025-04-11 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_alter_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
