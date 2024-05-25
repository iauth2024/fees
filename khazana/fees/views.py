from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum
from fees.forms import  PaymentForm
from .models import Student, Payment
from django.urls import reverse
from django.db.models import F
import csv
from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login page after logout
    else:
        # Handle GET requests by redirecting to the login page
        return redirect('login')

@login_required
def homepage(request):
    return render(request, 'homepage.html')


from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import PaymentForm
from .models import Student, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError  # Add this import statement

from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required  # Ensures only staff members can access the view
def download_payments(request):
    payments = Payment.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Receipt No', 'Student Admission No', 'Student Name', 'Amount', 'Date', 'Created By'])

    for payment in payments:
        writer.writerow([
            payment.receipt_no,
            payment.student.admission_number,
            payment.student.name,
            payment.amount,
            payment.date,
            payment.created_by.username if payment.created_by else ''  # Use username if available, else empty string
        ])

    return response


@login_required
def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            admission_number = form.cleaned_data['admission_number']
            student = Student.objects.get(admission_number=admission_number)
            total_due = calculate_total_due(student)
            amount_paid = form.cleaned_data['amount_paid']
            
            # Ensure the amount to pay is less than or equal to total due
            if 0 < amount_paid <= total_due:
                receipt_number = form.cleaned_data['receipt_number']
                created_by = request.user
                
                try:
                    # Save payment data to the database
                    payment = Payment.objects.create(
                        student=student,
                        amount=amount_paid,
                        receipt_no=receipt_number,
                        created_by=created_by
                    )
                    # Redirect to payment success page with admission number as a query parameter
                    return redirect(reverse('payment_success') + f'?admission_number={admission_number}')
                except IntegrityError:
                    # Handle duplicate receipt number error
                    messages.error(request, "A payment with the same receipt number already exists. Please enter a unique receipt number.")
            else:
                messages.error(request, "You cannot make 0 payment or more than the total due amount. Please pay the correct amount.")
    else:
        form = PaymentForm()

    return render(request, 'make_payment.html', {'form': form})

from .forms import PaymentUploadForm
from .models import Payment
import pandas as pd

from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)  # Ensure only admin users can access this view
def upload_payments(request):
    if request.method == 'POST':
        form = PaymentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)  # Assuming the data is in the first sheet
            
            # Process each row of the DataFrame
            for index, row in df.iterrows():
                receipt_no = row['Receipt No']
                student_admission_no = row['Student Admission No']
                amount = row['Amount']
                date = row['Date']
                created_by_username = row['Created By']  # Assuming this is a username
                
                # Create and save Payment instance
                payment = Payment(
                    receipt_no=receipt_no,
                    student=Student.objects.get(admission_number=student_admission_no),
                    amount=amount,
                    date=date,
                    created_by=User.objects.get(username=created_by_username)
                )
                payment.save()
            
            return HttpResponse('Payments uploaded successfully')
    else:
        form = PaymentUploadForm()
    return render(request, 'upload_payments.html', {'form': form})



def calculate_total_due(student):
    # Placeholder function to calculate total due for a student
    total_fees = student.total_fees  # Assuming you have a field named 'total_fees' in your Student model
    total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
    total_due = total_fees - total_paid
    return total_due

def payment_success(request):
    admission_number = request.GET.get('admission_number')
    try:
        student = Student.objects.get(admission_number=admission_number)
        payment_details = Payment.objects.filter(student=student).order_by('-date')
        return render(request, 'payment_success.html', {
            'student': student,
            'payment_details': payment_details
        })
    except Student.DoesNotExist:
        return render(request, 'payment_success.html', {
            'error_message': 'No payment found for the provided admission number'
        })


def get_student_details(request):
    if request.method == 'GET':
        admission_number = request.GET.get('admission_number')
        try:
            student = Student.objects.get(admission_number=admission_number)
            total_fees_paid = sum(payment.amount for payment in student.payment_set.all())
            total_due = student.total_fees - total_fees_paid
            months_paid = total_fees_paid / student.monthly_fees
            # Round off to 2 decimal places for monetary values
            total_fees_paid = round(total_fees_paid)
            total_due = round(total_due)
            # Round off to 1 decimal place for months_paid
            months_paid = round(months_paid, 1)
            data = {
                'name': student.name,
                'phone': student.phone,
                'course': student.course,
                'branch': student.branch,
                'monthly_fees': int(student.monthly_fees),  # Convert to integer to remove decimal places
                'total_fees': int(student.total_fees),  # Convert to integer to remove decimal places
                'total_paid': total_fees_paid,
                'total_due': total_due,
                'months_paid': months_paid
            }
            return JsonResponse({'success': True, 'student': data})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Admission number not found'}, status=404)


from django.shortcuts import render
from django.db.models import Sum
from .models import Student, Payment
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from xhtml2pdf import pisa # type: ignore
from django.template.loader import get_template
from django.db.models import Sum
from django.shortcuts import render


from .models import Student, Payment

def reports(request):
    # Fetch all students initially
    students = Student.objects.all()

    # Get unique choices for branch, class_darja, and course
    branch_choices = Student.BRANCH_CHOICES
    class_choices = Student.CLASS_CHOICES
    course_choices = Student.COURSE_CHOICES

    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if class_darja:
        students = students.filter(class_darja=class_darja)

    # Calculate months paid for each student and filter based on the provided months_paid
    filtered_students = []
    if months_paid.isdigit():
        months_paid = int(months_paid)
        for student in students:
            total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            paid_months = total_paid / student.monthly_fees if student.monthly_fees else 0
            if paid_months < months_paid:
                filtered_students.append(student)
    else:
        filtered_students = students

    # Calculate total fees paid and outstanding fees for each filtered student
    additional_info = []
    for student in filtered_students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
        'branch_choices': branch_choices,
        'class_choices': class_choices,
        'course_choices': course_choices,
        'course': course,
        'branch': branch,
        'selected_class_darja': class_darja,
        'selected_months_paid': months_paid,
    }
    return render(request, 'reports.html', context)



def generate_pdf(request):
    # Generate the PDF
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    if course:
        students = students.filter(course=course)
    if branch:
        students = students.filter(branch=branch)
    if class_darja:
        students = students.filter(class_darja=class_darja)
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = [student for student in students if (Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0) / student.monthly_fees >= months_paid]

    additional_info = []
    for student in students:
        total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0
        additional_info.append({
            'student': student,
            'monthly_fees': student.monthly_fees,
            'total_fees': student.total_fees,
            'total_paid': total_paid,
            'total_due': total_due,
            'months_paid': months_paid_count,
        })

    context = {
        'additional_info': additional_info,
    }

    template_path = 'pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from .models import Student, Payment

def generate_excel(request):
    # Generate the Excel
    students = Student.objects.all()
    # Get filter parameters from the request
    course = request.GET.get('course', '')
    branch = request.GET.get('branch', '')
    class_darja = request.GET.get('class_darja', '')
    months_paid = request.GET.get('months_paid', '')

    # Apply filters if provided
    
    if months_paid.isdigit():
        months_paid = int(months_paid)
        students = students.annotate(total_paid=Sum('payment__amount')).filter(total_paid__gte=F('monthly_fees') * months_paid)

    # Create a new Workbook object
    wb = Workbook()

    # Create a worksheet
    ws = wb.active

    # Add headers to the worksheet
    headers = ['Admission Number', 'Name', 'Course', 'Branch', 'Class', 'Monthly Fees', 'Total Fees', 'Total Paid', 'Total Due', 'Months Paid']
    ws.append(headers)

    # Add student data to the worksheet
    for student in students:
        total_paid = student.payment_set.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
        total_due = student.total_fees - total_paid
        months_paid_count = total_paid / student.monthly_fees if student.monthly_fees != 0 else 0

        row_data = [
            student.admission_number,
            student.name,
            student.course,
            student.branch,
            student.class_darja,
            student.monthly_fees,
            student.total_fees,
            total_paid,
            total_due,
            months_paid_count
        ]
        ws.append(row_data)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    # Save the workbook to the HTTP response
    wb.save(response)

    return response


from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'custom_password_reset.html'
    email_template_name = 'custom_password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'custom_password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'custom_password_reset_complete.html'

class CustomForgotPasswordView(auth_views.PasswordResetView):
    template_name = 'custom_forgot_password.html'  # Customize this template
    email_template_name = 'custom_password_reset_email.html'  # Use the same email template
    success_url = reverse_lazy('password_reset_done')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, FloatField
from django.db.models import ExpressionWrapper, F

@login_required
@staff_member_required  # Ensures only staff members can access the view

def summary(request):
    # Calculate total students
    total_students = Student.objects.count()

    # Calculate total fees
    total_fees = Student.objects.aggregate(total=Sum('total_fees'))['total'] or 0

    # Calculate total amount collected
    total_collected = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate total amount due
    total_due = total_fees - total_collected

    # Calculate students with no dues
    no_due_students = Student.objects.annotate(
        total_paid=Sum('payment__amount')
    ).filter(total_paid=F('total_fees')).count()

    context = {
        'total_students': total_students,
        'total_fees': total_fees,
        'total_collected': total_collected,
        'total_due': total_due,
        'no_due_students': no_due_students,
    }

    return render(request, 'summary.html', context)



@login_required
@staff_member_required
def summary(request):
    # Calculate total students
    total_students = Student.objects.count()

    # Calculate total fees
    total_fees = sum(student.total_fees for student in Student.objects.all())

    # Calculate total amount collected
    total_collected = sum(payment.amount for payment in Payment.objects.all())

    # Calculate total amount due
    total_due = total_fees - total_collected

    # Calculate students with zero due amount
    students_with_no_due = 0
    for student in Student.objects.all():
        total_paid_by_student = sum(payment.amount for payment in Payment.objects.filter(student=student))
        if student.total_fees == total_paid_by_student:
            students_with_no_due += 1

    context = {
        'total_students': total_students,
        'total_fees': total_fees,
        'total_collected': total_collected,
        'total_due': total_due,
        'students_with_no_due': students_with_no_due,
    }

    return render(request, 'summary.html', context)



@login_required

def user_payments(request):
    # Get payments made by the currently logged-in user
    user_payments = Payment.objects.filter(created_by=request.user).order_by('-date')

    context = {
        'user_payments': user_payments,
    }
    return render(request, 'user_payments.html', context)



from django.db.models import Sum

def student_payment_report(request):
    if request.method == 'POST':
        admission_number = request.POST.get('admission_number')
        try:
            student = Student.objects.get(admission_number=admission_number)
            payments = Payment.objects.filter(student=student).order_by('-date')
            
            # Fetch student attributes
            monthly_fee = student.monthly_fees
            total_fee = student.total_fees
            total_paid = Payment.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
            fee_due = total_fee - total_paid

            return render(request, 'student_payment_report.html', {
                'student': student,
                'payments': payments,
                'monthly_fee': monthly_fee,
                'total_fee': total_fee,
                'total_paid': total_paid,
                'fee_due': fee_due
            })
        except Student.DoesNotExist:
            return render(request, 'student_payment_report.html', {'error_message': 'Student not found'})
    else:
        return render(request, 'student_payment_report.html')
    


# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

# views.py
import pandas as pd
from .forms import UploadFileForm
from .models import Student

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from .forms import UploadFileForm
from .models import Student

@login_required
@user_passes_test(lambda u: u.is_staff)  # Ensure only admin users can access this view
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    student = Student(
                        admission_number=row['Admission Number'],
                        name=row['Name'],
                        phone=row['Phone'],
                        course=row['Course'],
                        class_darja=row['Class'],
                        branch=row['Branch'],
                        monthly_fees=row['Monthly Fees'],
                        student_type=row['Student Type']
                    )
                    student.save()
            # Similar processing for other file types like Google Sheets
            return HttpResponse('File uploaded successfully')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})
