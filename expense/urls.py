from django.urls import path

from . import views

urlpatterns = [
    path('', views.ExpenseList.as_view(), name="expense-list"),
    path('<int:id>/', views.ExpenseList.as_view(), name="expense-list"),
]