from django.contrib import admin
from .models import Student, Payment

class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'name', 'phone', 'course', 'branch', 'monthly_fees']
    search_fields = ['admission_number', 'name', 'phone']  # Add search fields for students

admin.site.register(Student, StudentAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'get_student_admission_number', 'amount', 'receipt_no', 'date', 'created_by']
    search_fields = ['student__admission_number', 'receipt_no']  # Add search fields for payments

    def get_student_name(self, obj):
        return obj.student.name
    get_student_name.short_description = 'Student Name'

    def get_student_admission_number(self, obj):
        return obj.student.admission_number
    get_student_admission_number.short_description = 'Admission Number'
