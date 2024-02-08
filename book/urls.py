from django.urls import path
from .views import BookList

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),
    path('<int:id>/', BookList.as_view(), name='book-list'),
]
