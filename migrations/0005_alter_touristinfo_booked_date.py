# Generated by Django 4.0.4 on 2022-06-20 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_touristinfo_tour_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristinfo',
            name='booked_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]