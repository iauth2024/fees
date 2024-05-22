from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from.views import upload_file, download_payments,upload_payments
from .views import reports, generate_pdf, generate_excel

from .views import user_payments, student_payment_report
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, summary
urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('', views.login_view, name='login'),
    path('upload/', upload_file, name='upload_file'),
    path('download-payments/', download_payments, name='download_payments'),
    path('upload-payments/', upload_payments, name='upload_payments'),
    path('logout/', views.logout_view, name='logout'),
    path('summary/', summary, name='summary'),
    path('reports/', reports, name='reports'),
    path('reports/pdf/', generate_pdf, name='generate_pdf'),
    path('reports/excel/', generate_excel, name='generate_excel'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('user/payments/', user_payments, name='user_payments'),
    path('student/payment/report/', student_payment_report, name='student_payment_report'),  # Add comma here
    path('reports/', views.reports, name='reports'),
    path('get_student_details/', views.get_student_details, name='get_student_details'),  # Remove extra space here
    path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot_password'),
    path('reset-password/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
