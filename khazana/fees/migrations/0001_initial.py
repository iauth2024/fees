# Generated by Django 5.0.4 on 2024-05-05 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_number', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('fees_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_received', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees.student')),
            ],
        ),
    ]
