from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
# Dont Repeat Yourself = DRY

from .forms import ContactForm
from blog.models import BlogPost, UserPayments
from django.contrib.auth import authenticate, login, logout


@login_required
def home_page(request):
    my_title = "Hello there...."
    qs = BlogPost.objects.all()[:5]
    user_list = []

    for obj in qs:
        user_data = {}
        user_data['user'] = obj
        payments = UserPayments.objects.filter(user = obj.user)
        user_data['payments'] = payments
        if payments:
            if payments.filter(status = False):
                user_data['verified'] = False
            else:
                user_data['verified'] = True
        else:
            user_data['verified'] = False
        # user_data['payment_count'] = payments.count()
        # print("user name:", obj.user.username, "payment count", payments.count())
        user_list.append(user_data)
    
    context = {"title": "Users List", 'user_list': user_list}
    print("logged in user is:", request.user)
    return render(request, "home.html", context)


@login_required
def logout_user(request):
    logout(request)
    # return redirect('login_user')
    return HttpResponseRedirect('/login')


@login_required
def about_page(request):
    return render(request, "about.html", {"title": "About"})



def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # return redirect('homepage')
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print('username', username)
            user_obj = authenticate(request, username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('homepage')
            else:
                return render(request,'login.html',{'form':form})
    else:
        form = AuthenticationForm()

    return render(request,'login.html',{'form':form})
    #return render(request, "login.html", {"title": "Login"})


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact us", 
        "form": form
    }
    return render(request, "form.html", context)



def example_page(request):
    context         =  {"title": "Example"}
    template_name   = "hello_world.html" 
    template_obj    = get_template(template_name)
    rendered_item   = template_obj.render(context)
    return HttpResponse(rendered_item)

