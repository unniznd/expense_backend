from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%B %d, %Y", read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        