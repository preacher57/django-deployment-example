from django.shortcuts import render
from django.urls import reverse

from basic_app.forms import UserForm,UserProfileInfoForm

#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request,'basic_app/index.html')

def register(request):

    #chech if user is registered
    registered = False


    #if request is post we grab information off forms
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #grab everything from base user form
            user = user_form.save()
            user.set_password(user.password)
            user.save()



            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                    'registered':registered
                    }
                  )



def user_login(request):

    # if user actually filled out form
    if request.method == 'POST':
        #called in 'username in login html
        username = request.POST.get('username')
        password = request.POST.get('password')

        #authenticates user
        user = authenticate(username=username, password=password)

        #checking if account is active
        if user:
            if user.is_active:
                login(request,user)
                #once user is logged in, send them back to homepage
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        #means request.method != post, so user hasn't submitted anything
        return render(request,'basic_app/login.html', {})




@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required()
def special(request):
    return HttpResponse("You are logged in, Nice!")

















































































