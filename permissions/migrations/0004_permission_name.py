# Generated by Django 5.2 on 2025-04-11 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_delete_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
