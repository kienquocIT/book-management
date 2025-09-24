from rest_framework.generics import get_object_or_404

from book.serializers import BookSerializer, BookUpdateSerializer
from book.models import Book

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BookList(APIView):
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get(self, request, id, format=None):
        book = Book.objects.all().get(id=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        book = get_object_or_404(Book, id=id)
        updateSerializer = BookUpdateSerializer(book, data=request.data)
        if updateSerializer.is_valid():
            updateSerializer.save()
            responseSerializer = BookSerializer(book)
            return Response(responseSerializer.data)
        return Response(updateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        book = Book.objects.all().get(id=id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)