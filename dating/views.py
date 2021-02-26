from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,ProfileForm,UserForm

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .filters import ProfileFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from .serializers import UserSerializer

from django.views.generic import DetailView, ListView

from .forms import ComposeForm

from .models import *
import random


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method =='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user + ', you can now login.')

                return redirect('login')
            else:
                messages.info(request,'Please check your info and try again.')


        context = {
            'form':form
        }
        return render(request,'dating/register.html',context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request,'Login successful , please set up your profile to help people find you.')
                return redirect('home')                
            else:
                messages.info(request, 'Username OR password is incorrect')
       





        context = {}
        return render(request,'dating/login.html', context)

@login_required(login_url='login')
def homepage(request):
    name = request.user
    profile_id = Profile.objects.all().exclude(user=name)

    MyFilter = ProfileFilter(request.GET, queryset=profile_id)
    # if request.user.is_active == True:
    #     print("active")
    # else:
    #     print("Not active")
    try:
        profile_id = MyFilter.qs
        profiles = random.choice(list(profile_id))
    except:
        messages.info(request,'No results found,try filtering again.')
        profile_id = Profile.objects.all()
        profiles = random.choice(list(profile_id))


    filform = MyFilter.form

    
    


    context = {
        'profiles':profiles,
        'filform':filform,
    }
    return render(request,'dating/home.html',context)

@login_required(login_url='login')
def searchpage(request):
    name = request.user
    profile_id = Profile.objects.all().exclude(user=name)
    no = 4
    profiles = random.sample(list(profile_id), no)
    
    length = len(profile_id) 
    
    if length > int(no):
       profiles = random.sample(list(profile_id), no)

    else:
        profiles = Profile.objects.all().exclude(user=name)



    


    context = {
        'profiles':profiles,
        
    }
    return render(request,'dating/search.html',context)
@login_required(login_url='login')
def userSettings(request):
    user = request.user
    setting = user.profile

    serializer = UserSerializer(setting, many=False)

    return JsonResponse(serializer.data, safe=False)
@login_required(login_url='login')
def updattheme(request):
    data = json.loads(request.body)
    theme = data['theme']
    user = request.user
    user.profile.value = theme
    user.profile.save() 
    print('request', theme)
    return JsonResponse('Updated..', safe = False)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    user = request.user.profile
    user2 = request.user
    p_form = ProfileForm(instance=user)
    u_form = UserForm(instance=user2)
    

    if request.method =='POST':
        p_form = ProfileForm(request.POST,request.FILES,instance=user)
        u_form = UserForm(request.POST,request.FILES,instance=user2)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request,'Profile updated!')
             


    context = {
        'p_form':p_form,
        'u_form':u_form
    }
    return render(request,'dating/profile.html',context)
    
@login_required(login_url='login')
def prof(request):

    return render(request,'dating/prof.html')

@login_required(login_url='login')
def Messagepage(request):
    thread = Thread.objects.by_user(request.user).order_by('-timestamp')
   
    name = request.user.username
    users = User.objects.all().exclude(username=name,password=request.user.password)

    msg = ChatMessage.objects.filter(user=request.user)
    
 

    context = {

        'thread':thread

    }

    return render(request,'dating/message.html',context)




class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'dating/chat.html'
    form_class = ComposeForm
    

    def get_success_url(self):
        return self.request.path

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)



