# Generated by Django 3.1.7 on 2021-04-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210418_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='cancel_date',
            field=models.CharField(max_length=50, null=True),
        ),
    ]