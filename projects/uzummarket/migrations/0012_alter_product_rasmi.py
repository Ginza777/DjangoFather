# Generated by Django 5.0.2 on 2024-04-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzummarket', '0011_remove_product_rasmi2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rasmi',
            field=models.ImageField(blank=True, null=True, upload_to='./static/product_images/'),
        ),
    ]
