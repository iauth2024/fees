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
    COURSE_CHOICES = [
        ('Mahade Ashraf', 'Mahade Ashraf'),
        ('معہد ابرار', 'معہد ابرار'),
        ('حفظ', 'حفظ'),
        ('ناظرہ', 'ناظرہ'),
        ('معہد علیم', 'معہد علیم'),
        ('معہد قاسم', 'معہد قاسم'),
    ]
    
    CLASS_CHOICES = [
        ('INTER - I', 'INTER - I'),
        ('INTER - II', 'INTER - II'),
        ('B.COM -I', 'B.COM - I'),
        ('B.COM -II', 'B.COM - II'),
        ('B.COM -III', 'B.COM - III'),  
        ('Awwal (Alif)', 'اول (الف)'),
        ('Awwal (Baa)', 'اول (ب)'),
        ('Awwal (Jeem)', 'اول (ج)'),
        ('Duwwam (Alif)', 'دوم (الف)'),
        ('Duwwam (Baa)', 'دوم (ب)'),
        ('Suwwam (Alif)', 'سوم (الف)'),
        ('Suwwam (Baa)', 'سوم (ب)'),
        ('Suwwam (Jeem)', 'سوم (ج)'),
        ('Chahrum (Alif)', 'چهارم (الف)'),
        ('Chahrum (Baa)', 'چهارم (ب)'),
        ('Panjum', 'پنجم'),
        ('Mouqoof Alai', 'موقوف علیہ'),
        ('Daur-e-Hadees', 'دورہ حدیث'),
        ('Edadiya School (Alif)', 'ادادیہ اسکول (الف)'),
        ('Edadiya School (Baa)', 'ادادیہ اسکول (ب)'),
        ('Awwal School (Alif)', 'اول اسکول (الف)'),
        ('Awwal School (Baa)', 'اول اسکول (ب)'),
        ('Duwwam School (Alif)', 'دوم اسکول (الف)'),
        ('Duwwam School (Baa)', 'دوم اسکول (ب)'),
        ('Suwwam', 'سوم'),
        ('Chahrum', 'چهارم'),
        ('Hifz-Alif','Hifz-Alif'),
        ('Hifz-Baa','Hifz-Baa'),
        ('Hifz-Jeem','Hifz-Jeem'),
        ('Hifz-Daal','Hifz-Daal'),
        ('Hifz-Zaa','Hifz-Zaa'),
        ('Hifz-Haa','Hifz-Haa'),
        ('Hifz-Haah','Hifz-Haah'),
        ('Hifz-Waav','Hifz-Waav'),
        ('Nazira-Alif','Nazira-Alif'),
        ('Nazira-Baa','Nazira-Baa'),
        ('Nazira-Jeem','Nazira-Jeem'),
        ('Nazira-Daal','Nazira-Daal'),
       

    ]
    
    ADMISSION_CHOICES = [
        ('boarder', 'Boarder'),
        ('day_scholar', 'Day Scholar'),
    ]
    
    admission_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, blank=True, null=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    class_darja = models.CharField(max_length=100, choices=CLASS_CHOICES)
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