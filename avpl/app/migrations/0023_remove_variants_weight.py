# Generated by Django 3.1.7 on 2021-04-27 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_variants_fake_real_var_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variants',
            name='weight',
        ),
    ]
