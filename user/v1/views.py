from ..models import User
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

def list(request):
    print("List users")
    users = User.objects.all()
    template = loader.get_template("user/list.html")
    context = {
        'users_list': users,
    }
    print(context)
    return HttpResponse(template.render(context, request)) 

def detail(request, user_id):
    user = User.objects.filter(id=user_id).first()
    template = loader.get_template("user/detail.html")
    context = {
        'user': user,
    }
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        valid_email = User.objects.filter(email=email).exclude(id=user_id).first()
        if valid_email:
            context['user'] = None
            context['error'] = "Email already exists"
            return HttpResponse(template.render(context, request))

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save(update_fields=['email', 'first_name', 'last_name'])
        return redirect('UserList')
    elif request.method == "GET":
        return HttpResponse(template.render(context, request))

def create(request):
    print(request.POST)
    template = loader.get_template("user/create.html")

    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')

        valid_username = User.objects.filter(username=username).first()
        valid_email = User.objects.filter(email=email).first()

        if valid_username:
            context = {
                'error': "Username already exists"
            }
            return HttpResponse(template.render(context, request))
        if valid_email:
            context = {
                'error': "Email already exists"
            }
            return HttpResponse(template.render(context, request))

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()
        return redirect('UserList')
    else:
        context = {}
        return HttpResponse(template.render(context, request))
    
def delete(request, user_id):
    user = User.objects.filter(id=user_id).first()
    template = loader.get_template("user/delete.html")
    if request.method == "POST":
        user.delete()   
        return redirect('UserList')
    elif request.method == "GET":
        context = {
            'user': user,
        }
        return HttpResponse(template.render(context, request))








