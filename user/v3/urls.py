from django.urls import path
from .views import user_list, user_detail, register_user, login_user

urlpatterns = [
    path('', user_list, name="UserList"),
    path('<int:pk>', user_detail, name="UserDetail"),
    path('register', register_user, name="UserRegister"),
    path('login', login_user, name="UserLogin"),
]
