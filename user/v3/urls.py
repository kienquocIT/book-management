from django.urls import path
from .views import user_list, user_detail

urlpatterns = [
    path('', user_list, name="UserList"),
    path('<int:pk>', user_detail, name="UserDetail")
]
