import uuid

from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from book.serializers import BookListSerializer, BookUpdateSerializer, BookCreateSerializer, BookDetailSerializer, \
    BookUploadDemoFileSerializer, StoreListSerializer, StoreCreateSerializer, StoreUpdateSerializer, \
    StoreTransBookToStoreSerializer, BookMultiSaleSerializer
from book.serializers import AuthorListSerializer, AuthorUpdateSerializer, AuthorCreateSerializer, AuthorDetailSerializer
from book.models import Book, Author, Menu, Store

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from book.tasks import send_new_book_via_email
from shared.pagination import LargeResultsSetPagination


# Book
class BookList(APIView):
    pagination_class = LargeResultsSetPagination
    search_fields = ['title', 'author__first_name', 'author__last_name']

    def get(self, request, format=None):
        books = Book.objects.all().prefetch_related('menus', 'authors')

        author_ids = request.GET.get('author_ids')
        if author_ids:
            try:
                author_ids_list = [
                    uuid.UUID(aid.strip()) for aid in author_ids.split(',')
                    if aid.strip()
                ]
                books = books.filter(authors__id__in=author_ids_list).distinct().prefetch_related('menus', 'authors')
            except ValueError:
                return Response(
                    {"error": ""},
                    status=status.HTTP_400_BAD_REQUEST
                )
        search_query = request.GET.get('search', None)
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(authors__first_name__icontains=search_query) |
                Q(authors__last_name__icontains=search_query)
            )

        paginator = self.pagination_class()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookListSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            detailSerializer = BookDetailSerializer(book)
            send_new_book_via_email.delay(book.title)
            return Response(detailSerializer.data, status=status.HTTP_201_CREATED)
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
            responseSerializer = BookDetailSerializer(book)
            return Response(responseSerializer.data)
        return Response(updateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        Book.objects.all().filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookUploadView(generics.UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = BookUploadDemoFileSerializer
    queryset = Book.objects.all()
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(file=self.request.data.get('file'))

# Author
class AuthorList(APIView):
    pagination_class = LargeResultsSetPagination
    search_fields = ['first_name', 'last_name']

    def get(self, request, format=None):
        authors = Author.objects.all().prefetch_related('books')

        search_query = request.GET.get('search', None)
        if search_query:
            authors = authors.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        paginator = self.pagination_class()
        paginated_authors = paginator.paginate_queryset(authors, request)
        serializer = AuthorListSerializer(paginated_authors, many=True)

        return paginator.get_paginated_response(serializer.data)

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

# Stores
class StoreList(APIView):
    def get(self, request, format=None):
        store = Store.objects.all()
        serializer = StoreListSerializer(store, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StoreCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreDetail(APIView):
    def get(self, request, id, format=None):
        store = get_object_or_404(Store, id=id)
        serializer = StoreListSerializer(store)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        store = get_object_or_404(Store, id=id)
        updateSerializer = StoreUpdateSerializer(store, data=request.data)
        if updateSerializer.is_valid():
            updateSerializer.save()
            responseSerializer = StoreUpdateSerializer(store)
            return Response(responseSerializer.data)
        return Response(updateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        store = get_object_or_404(Store, id=id)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StoreTransferBook(APIView):
    def post(self, request, format=None):
        serializer = StoreTransBookToStoreSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StoreSaleBook(APIView):
    def post(self, request, format=None):
        serializer = BookMultiSaleSerializer(data={'sales': request.data})
        if serializer.is_valid():
            results = serializer.save()
            return Response(results, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


