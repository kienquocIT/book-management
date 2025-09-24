from django.urls import path
from .views import list, detail, create, delete
urlpatterns = [
    path('', list, name='UserList'),
    path('<int:user_id>', detail, name='UserDetail'),
    path('create', create, name='UserCreate'),
    path('delete/<int:user_id>', delete, name='UserDelete'),   
]