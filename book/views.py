from rest_framework.generics import get_object_or_404

from book.serializers import BookListSerializer, BookUpdateSerializer, BookCreateSerializer, BookDetailSerializer
from book.serializers import AuthorListSerializer, AuthorUpdateSerializer, AuthorCreateSerializer, AuthorDetailSerializer
from book.models import Book, Author

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Book
class BookList(APIView):
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get(self, request, id, format=None):
        book = Book.objects.all().get(id=id)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        book = get_object_or_404(Book, id=id)
        updateSerializer = BookUpdateSerializer(book, data=request.data)
        if updateSerializer.is_valid():
            updateSerializer.save()
            responseSerializer = BookUpdateSerializer(book)
            return Response(responseSerializer.data)
        return Response(updateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        Book.objects.all().filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Author
class AuthorList(APIView):
    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorListSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetail(APIView):
    def get(self, request, id, format=None):
        author = get_object_or_404(Author, id=id)
        serializer = AuthorDetailSerializer(author)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        author = get_object_or_404(Author, id=id)
        updateSerializer = AuthorUpdateSerializer(author, data=request.data)
        if updateSerializer.is_valid():
            updateSerializer.save()
            responseSerializer = AuthorUpdateSerializer(author)
            return Response(responseSerializer.data)
        return Response(updateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        author = get_object_or_404(Author, id=id)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

