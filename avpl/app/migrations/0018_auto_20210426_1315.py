# Generated by Django 3.1.7 on 2021-04-26 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20210425_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_fake',
            name='stor_details',
        ),
        migrations.RemoveField(
            model_name='product_fake',
            name='user',
        ),
        migrations.RemoveField(
            model_name='variants_fake',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order_detail',
        ),
        migrations.DeleteModel(
            name='Product_fake',
        ),
        migrations.DeleteModel(
            name='Variants_fake',
        ),
    ]