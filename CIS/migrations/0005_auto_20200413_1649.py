# Generated by Django 3.0.5 on 2020-04-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CIS', '0004_remove_product_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(max_length=100),
        ),
    ]
