# Generated by Django 5.0.2 on 2024-04-01 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzummarket', '0007_alter_product_rasmi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rasmi',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]