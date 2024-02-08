
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', include('book.urls')),
    path('api/expenses/', include('expense.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]
