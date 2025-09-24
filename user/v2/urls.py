from django.urls import path
from .views import UserList, UserCreate, DetailUpdateUser, DeleteUser
app_name = "user_v2"

urlpatterns = [
    path("", UserList.as_view(), name='UserList'),
    path("create", UserCreate.as_view(), name='UserCreate'),
    path('<int:pk>', DetailUpdateUser.as_view(), name='UserDetail'),
    path('delete/<int:pk>', DeleteUser.as_view(), name='UserDelete'),   
]