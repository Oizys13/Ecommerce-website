# Generated by Django 4.0.3 on 2022-05-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_whishlist_product_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]
