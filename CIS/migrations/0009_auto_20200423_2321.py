# Generated by Django 3.0.5 on 2020-04-23 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CIS', '0008_auto_20200423_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='Country',
            new_name='country',
        ),
    ]