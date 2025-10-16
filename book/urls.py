from django.urls import path
from book.views import BookList, BookDetail, AuthorList, AuthorDetail, BookUploadView, StoreList, StoreDetail, \
    StoreTransferBook, StoreSaleBook

urlpatterns = [
    # Book
    path('', BookList.as_view(), name="BookList"),
    path('<uuid:id>', BookDetail.as_view(), name="BookDetail"),
    path('<uuid:pk>/upload', BookUploadView.as_view(), name="BookUpload"),
    # Author
    path('authors', AuthorList.as_view(), name="AuthorList"),
    path('authors/<uuid:id>', AuthorDetail.as_view(), name="AuthorDetail"),
    path('stores', StoreList.as_view(), name="StoreList"),
    path('stores/<uuid:id>', StoreDetail.as_view(), name="StoreDetail"),
    path('stores/trans', StoreTransferBook.as_view(), name="StoreTransferBook"),
    path('stores/sale', StoreSaleBook.as_view(), name="StoreSaleBook"),
]