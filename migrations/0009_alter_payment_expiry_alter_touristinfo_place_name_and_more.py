# Generated by Django 4.0.4 on 2022-06-24 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_touristinfo_booked_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='expiry',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='touristinfo',
            name='place_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='touristinfo',
            name='user_name',
            field=models.CharField(max_length=100),
        ),
    ]