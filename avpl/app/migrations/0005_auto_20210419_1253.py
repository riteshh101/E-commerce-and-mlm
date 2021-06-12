# Generated by Django 3.1.7 on 2021-04-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_order_detail_order_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_detail',
            name='order_status',
            field=models.CharField(choices=[('Deliver', 'Deliver'), ('Booked', 'Booked'), ('Cancel', 'Cancel')], default='Booked', max_length=100),
        ),
    ]
