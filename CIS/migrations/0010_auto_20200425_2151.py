# Generated by Django 3.0.5 on 2020-04-25 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CIS', '0009_auto_20200423_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='country',
            new_name='municipality',
        ),
    ]
