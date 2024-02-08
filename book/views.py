from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

class BookList(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        is_returned_param = self.request.query_params.get('isReturned', None)

        if is_returned_param is not None:
            # Filter based on isReturned parameter
            return Book.objects.filter(isReturned=is_returned_param)
        
        return Book.objects.all()


    def get(self, request, id=None):
        if id:
            try:
                book = Book.objects.get(id=id)
            except Book.DoesNotExist:
                return Response({
                    "status":False,
                    "message":"Book not found"
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(book)
            return Response({
                "status":True,
                "data":serializer.data
            })
        else:
            books = self.get_queryset()
            serializer = BookSerializer(books, many=True)
            return Response({
                "status":True,
                "totalCount":books.count(),
                "returnCount":books.filter(isReturned=True).count(),
                "data":serializer.data
            })

    def post(self, request):
        serializer = BookSerializer(data=request.data)
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
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({
                "status":False,
                "message":"Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data, partial=True)
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
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response({
                "status":False,
                "message":"Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response({
            "status":True,
        }, status=status.HTTP_204_NO_CONTENT)
    
    