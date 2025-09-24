from django.urls import path
from book.views import BookList, BookDetail

urlpatterns = [
    path('', BookList.as_view(), name="BookList"),
    path('<int:id>', BookDetail.as_view(), name="BookDetail"),
]