# Generated by Django 4.0.3 on 2022-05-24 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_product_show_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_validated',
        ),
    ]