# Generated by Django 3.1.7 on 2021-04-20 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210419_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='variants',
            name='after_discount_price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='variants',
            name='variant_discount',
            field=models.FloatField(null=True),
        ),
    ]
