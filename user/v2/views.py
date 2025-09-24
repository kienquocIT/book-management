from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..models import User
from django.urls import reverse_lazy

class UserList(ListView):
    model = User
    template_name = "user/list.html"
    context_object_name = "users_list"
    queryset = User.objects.all()

class UserCreate(CreateView):
    model = User
    fields = "__all__"
    template_name = "user/create.html"
    success_url = reverse_lazy("user_v2:UserList")

class DetailUpdateUser(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = "user/detail.html"
    def get_success_url(self):
        return reverse_lazy("user_v2:UserDetail", kwargs = {"pk": self.object.pk})
    
class DeleteUser(DeleteView):
    model = User
    template_name = "user/delete.html"
    def get_success_url(self):
        return reverse_lazy("user_v2:UserList")
