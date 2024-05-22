# models.py

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    BRANCH_CHOICES = [
        ('Khaja Bagh', 'Khaja Bagh'),
        ('Akber Bagh', 'Akber Bagh'),
        ('Ghatkesar', 'Ghatkesar'),
        ('Bandlaguda', 'Bandlaguda'),
    ]
    CLASS_CHOICES = [
        ('INTER - I', 'INTER - I'),
        ('INTER - II', 'INTER - II'),
        ('Third', 'Third'),
    ]
    
    ADMISSION_CHOICES = [
        ('boarder', 'Boarder'),
        ('day_scholar', 'Day Scholar'),
    ]
    
    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, blank=True, null=True)
    course = models.CharField(max_length=100)
    class_darja = models.CharField(max_length=20, choices=CLASS_CHOICES)
    branch = models.CharField(max_length=100, choices=BRANCH_CHOICES)
    monthly_fees = models.DecimalField(max_digits=10, decimal_places=2)
    student_type = models.CharField(max_length=20, choices=ADMISSION_CHOICES)
    
    @property
    def total_fees(self):
        return self.monthly_fees * 12


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_no = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.receipt_no