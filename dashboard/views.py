from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.http import HttpResponse
from django.db import models

import csv

from book.models import Book
from expense.models import Expense
from expense.serializers import ExpenseSerializer

class Dashboard(ListAPIView):
    def get(self, request):
        books = Book.objects.all()
        expenses = Expense.objects.all()
        totalExpense = 0
        for expense in expenses:
            totalExpense += expense.amount
        
        totalBookAmount = 0
        for book in books:
            totalBookAmount += book.amount
        
        return Response({
            "status":True,
            "totalBookAmount":totalBookAmount,
            "totalExpense":totalExpense
        })

@api_view(['GET'])
def getDateWiseExpense(request):
    expense = Expense.objects.all()
    data = {}
    expense_serializer = ExpenseSerializer(expense, many=True)
    for exp in expense_serializer.data:
        date = exp['date']
        if date in data:
            data[date]['amount'] += exp['amount']
            data[date]['data'].append(exp)
        else:
            data[date] = {
                "amount":exp['amount'],
                "data":[exp,]
            }
    
    return Response({
        "status":True,
        "data":data
    })

def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ethalattukavu_temple_report.csv"'

    writer = csv.writer(response)

    # Add letter pad information
    writer.writerow(['Ethalattukavu Temple'])
    writer.writerow([])

    # Total income and expense
    total_income = Book.objects.aggregate(total=models.Sum('amount'))['total'] or 0
    total_expense = Expense.objects.aggregate(total=models.Sum('amount'))['total'] or 0
    writer.writerow(['Total Income', 'Total Expense'])
    writer.writerow([total_income, total_expense])
    writer.writerow([])

    # Table for date-wise expense
    writer.writerow(['Date', 'Total Amount on Date'])
    expenses_by_date = Expense.objects.values('date').annotate(total_amount=models.Sum('amount'))
    for expense in expenses_by_date:
        writer.writerow([expense['date'], expense['total_amount']])
    writer.writerow([])

    # Table for all book data
    writer.writerow(['Book Number', 'Name', 'Amount', 'Page Left', 'Is Returned', 'Last Updated'])
    books = Book.objects.all()
    for book in books:
        writer.writerow([book.bookNumber, book.name, book.amount, book.pageLeft, book.isReturned, book.lastUpdated])
    writer.writerow([])

    # Table for all expenses
    expenses = Expense.objects.all()
    writer.writerow(['Expense Name', 'Amount', 'Date', 'By Whom', 'Last Updated'])
    for expense in expenses:
        writer.writerow([expense.name, expense.amount, expense.date, expense.byWhom, expense.lastUpdated])

    return response