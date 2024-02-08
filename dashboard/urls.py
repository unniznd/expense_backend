from django.urls import path

from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),
    path('datewise-expense/', views.getDateWiseExpense, name='getDateWiseExpense'),
    path('csv/', views.generate_csv, name='generate_pdf_report'),
   
]