# Generated by Django 3.1.1 on 2021-10-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_receiving',
            name='purchase_price',
            field=models.IntegerField(default=0),
        ),
    ]
