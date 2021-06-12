# Generated by Django 3.1.7 on 2021-04-26 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_auto_20210426_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_fake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('subcategory', models.CharField(max_length=100)),
                ('brand_name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('discount_percent', models.FloatField(blank=True, null=True)),
                ('gst_percent', models.FloatField(blank=True, null=True)),
                ('variant', models.CharField(max_length=10)),
                ('image', models.ImageField(null=True, upload_to='product_fake')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('Buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stor_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor_store_detail')),
            ],
        ),
        migrations.CreateModel(
            name='Variants_fake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('image_fornt', models.ImageField(null=True, upload_to='image_front_fake')),
                ('image_back', models.ImageField(null=True, upload_to='image_back_fake')),
                ('image_side', models.ImageField(null=True, upload_to='image_side_fake')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('point_value', models.FloatField(null=True)),
                ('after_discount_price', models.FloatField(null=True)),
                ('variant_discount', models.FloatField(null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product_fake')),
            ],
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=200)),
                ('order_id', models.CharField(max_length=200)),
                ('signature', models.CharField(max_length=200)),
                ('order_status', models.CharField(choices=[('Deliver', 'Deliver'), ('Booked', 'Booked'), ('Cancel', 'Cancel')], default='Booked', max_length=100)),
                ('delivery_status', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('cancel_date', models.CharField(max_length=50, null=True)),
                ('time_slot', models.CharField(max_length=100, null=True)),
                ('order_mode', models.CharField(choices=[('Self_Picking', 'Self_Pickig'), ('Delivery', 'Delivery')], default='Order', max_length=40)),
                ('price', models.FloatField()),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.delivery_address')),
                ('item', models.ManyToManyField(to='app.Variants_fake')),
                ('store_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vendor_store_detail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
