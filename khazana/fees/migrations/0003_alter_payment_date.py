# Generated by Django 5.0.4 on 2024-05-07 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0002_rename_amount_received_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(),
        ),
    ]
