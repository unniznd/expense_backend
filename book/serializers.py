from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    lastUpdated = serializers.DateTimeField(format="%B %d, %Y", read_only=True)
    class Meta:
        model = Book
        fields = '__all__'