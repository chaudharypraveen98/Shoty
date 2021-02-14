from django.views import generic
from django.contrib import messages
from.models import Album, Song, Contact_Us
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from .forms import UserForm
from django.contrib.auth.models import User
from .login import LoginForm
from myfirstproject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.forms import modelformset_factory


class IndexView(generic.ListView):
    template_name = "music/index.html"
    context_object_name = "all_albums"
    success_url = "music/index.html"

    def get_queryset(self):
        return Album.objects.all()

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Contact_Us(name=name, email=email,
                   subject=subject, message=message).save()
        send_mail("Thank you for your valuable feedback", "we are hoping to look ahead of your problem",
                  EMAIL_HOST_USER, [email], fail_silently=False)
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
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'
    # it will get the form

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    # it will submit the form
    def post(self, request):
        if User.objects.filter(username=request.POST.get("username")).exists():
            return redirect('music:login')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Django first validate and clean the data.
            # malicious user to wreak havoc on your site.
            # browser would everything as strings. When Django cleans the data it automatically converts data -appropriate type.validated data is commonly known as cleaned data.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # you can't set password="1233" because the password stored is in encription
            user.set_password(password)
            form.save()

            # it will check the database
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
            # if the required field are not valid it will return the field
        return render(request, self.template_name, {"form": form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "music/user_form.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('music:index')
            print(user)
        return render(request, self.template_name, {"form": form})


def logout_view(request):
    logout(request)
    return redirect('music:index')


def product_view(request, pk):
    # getting primary key as an argument form the url via detail template
    # getting particular album via pk
    album = Album.objects.get(pk=pk)

    # modelformset_factory is used when we want to make objects of a particular class
    SongFormset = modelformset_factory(
        Song, fields=('song_title', 'song_logo'))

    # queryset is the collection of objects which are already in that class
    formset = SongFormset(queryset=Song.objects.filter(album__id=pk))
    if request.method == 'POST':
        formset = SongFormset(
            request.POST, queryset=Song.objects.filter(album__id=pk))

        # formset.errors is used only for debgging purpose
        print(formset.errors)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit=False)
                # making relation
                instance.album = album
                instance.save()

            # we are passing extra argument which is the pk of the class instance which is need in detail template
            return redirect('music:detail', pk=pk)

    return render(request, 'music/edit.html', {"formset": formset})
