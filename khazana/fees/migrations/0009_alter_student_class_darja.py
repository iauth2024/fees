# Generated by Django 5.0.4 on 2024-05-21 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0008_alter_payment_receipt_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='class_darja',
            field=models.CharField(choices=[('INTER - I', 'INTER - I'), ('INTER - II', 'INTER - II'), ('Third', 'Third')], max_length=20),
        ),
    ]
