# Generated by Django 3.0.5 on 2020-04-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CIS', '0006_auto_20200417_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
