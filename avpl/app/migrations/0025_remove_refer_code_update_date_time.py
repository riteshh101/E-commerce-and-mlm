# Generated by Django 3.1.7 on 2021-04-28 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_order_detail_oreder_cancel_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refer_code',
            name='update_date_time',
        ),
    ]
