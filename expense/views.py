from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Expense
from .serializers import ExpenseSerializer, ExpenseCreateSerializer

class ExpenseList(ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.all()

    def get(self, request, id=None):
        if id:
            try:
                expense = Expense.objects.get(id=id)
            except Expense.DoesNotExist:
                return Response({
                    "status":False,
                    "message":"Expense not found"
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = ExpenseSerializer(expense)
            return Response({
                "status":True,
                "data":serializer.data
            })
        else:
            expenses = self.get_queryset()
            totalAmount = 0
            for expense in expenses:
                totalAmount += expense.amount
            serializer = ExpenseSerializer(expenses, many=True)
            return Response({
                "status":True,
                "totalCount":expenses.count(),
                "totalAmount":totalAmount,
                "data":serializer.data
            })

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status":False,
            "message":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            expense = Expense.objects.get(id=id)
        except Expense.DoesNotExist:
            return Response({
                "status":False,
                "message":"Expense not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseCreateSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":True,
            })
        return Response({
            "status":False,
            "message":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            expense = Expense.objects.get(id=id)
        except Expense.DoesNotExist:
            return Response({
                "status":False,
                "message":"Expense not found"
            }, status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response({
            "status":True,
        }, status=status.HTTP_204_NO_CONTENT)