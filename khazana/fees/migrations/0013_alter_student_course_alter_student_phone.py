# Generated by Django 5.0.6 on 2024-05-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0012_alter_student_class_darja'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(choices=[('Mahade Ashraf', 'Mahade Ashraf'), ('معہد ابرار', 'معہد ابرار'), ('حفظ', 'حفظ'), ('ناظرہ', 'ناظرہ'), ('معہد علیم', 'معہد علیم'), ('معہد قاسم', 'معہد قاسم')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]