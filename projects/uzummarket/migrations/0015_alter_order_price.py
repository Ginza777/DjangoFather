# Generated by Django 5.0.2 on 2024-04-01 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzummarket', '0014_alter_product_rasmi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(),
        ),
    ]
