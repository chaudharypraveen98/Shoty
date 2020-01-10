'''this view is a class based view.
A view is a callable which takes a request and returns a response.
This can be more than just a function, and Django provides an example of 
some classes which can be used as views. These allow you to structure 
your views and reuse code by harnessing inheritance and mixins.
There are also some generic views for tasks which we’ll get to later, 
but you may want to design your own structure of reusable views
which suits your use case.'''

from django.views import generic
from django.contrib import messages
from.models import Album,Song,Contact_Us
from django.views.generic.edit import CreateView,UpdateView,DeleteView #for editing the data
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.views.generic import View,FormView
from .forms import UserForm
from django.contrib.auth.models import User
from .login import LoginForm
from myfirstproject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.generic.base import TemplateView

class IndexView(generic.ListView):
  template_name = "music/index.html"
  context_object_name = "all_albums"
  success_url = "music/index.html"
  def get_queryset(self):
    return Album.objects.all()
  def post(self,request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    message = request.POST.get("message")
    Contact_Us(name=name,email=email,subject=subject,message=message).save()
    send_mail("Thank you for your valuable feedback","we are hoping to look ahead of your problem",EMAIL_HOST_USER,[email],fail_silently=False)
    messages.success(request, 'Form submission successful')
    return redirect('music:index')

class DetailView(generic.DetailView):
  model = Album
  template_name = "music/detail.html"
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_list'] = Song.objects.filter(album=self.object)
        return context

class Music(TemplateView):

    template_name = "music/song.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = Album.objects.all()
        context['song_list'] = Song.objects.all()
        return context
class AlbumCreate(CreateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']
  
class AlbumDelete(DeleteView):
  model = Album
  success_url = reverse_lazy('music:index')

class UserFormView(View):
  form_class = UserForm
  template_name = 'music/registration_form.html'
  #it will get the form
  def get(self,request):
    form = self.form_class(None)
    return render(request,self.template_name,{"form":form})

  #it will submit the form
  def post(self,request):
    if User.objects.filter(username=request.POST.get("username")).exists():
    	return redirect('music:login')
    form = self.form_class(request.POST)
    if form.is_valid():
      user = form.save(commit = False)
      #Django first validate and clean the data. 
      #malicious user to wreak havoc on your site.
      #browser would everything as strings. When Django cleans the data it automatically converts data -appropriate type.validated data is commonly known as cleaned data. 
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      #you can't set password="1233" because the password stored is in encription
      user.set_password(password)
      form.save()

      #it will check the database
      user = authenticate(username=username,password=password)
      print(user)
      if user is not None:
        if user.is_active:
          login(request,user)
          return redirect('music:index')
      #if the required field are not valid it will return the field
    return render(request,self.template_name,{"form":form})
class LoginView(FormView):
  form_class = LoginForm
  template_name = "music/user_form.html"
  def get(self,request):
    form = self.form_class(None)
    return render(request,self.template_name,{"form":form})
  def post(self,request):
    form = self.form_class(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      print(username,password)
      user = authenticate(username=username,password=password)
      if user is not None:
        login(request,user)
        return redirect('music:index')
      print(user)
    return render(request,self.template_name,{"form":form})

def logout_view(request):
  logout(request)
  return redirect('music:index')