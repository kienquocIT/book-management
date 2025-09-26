from django.urls import path
from book.views import BookList, BookDetail, AuthorList, AuthorDetail

urlpatterns = [
    path('', BookList.as_view(), name="BookList"),
    path('<uuid:id>', BookDetail.as_view(), name="BookDetail"),
    path('authors', AuthorList.as_view(), name="AuthorList"),
    path('authors/<uuid:id>', AuthorDetail.as_view(), name="AuthorDetail"),
]