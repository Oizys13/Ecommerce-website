# Generated by Django 4.0.3 on 2022-05-24 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_product_whishlist_alter_product_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='whishlist',
            new_name='wishlist',
        ),
    ]