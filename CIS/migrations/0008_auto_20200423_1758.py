# Generated by Django 3.0.5 on 2020-04-23 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CIS', '0007_customer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
