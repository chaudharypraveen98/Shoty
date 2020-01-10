from django.conf.urls import url
from . import views

app_name='music'

urlpatterns = [
    #music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #music/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #music/login
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    #music/logout
    url(r'^logout/$', views.logout_view, name='logout'),
    #music/music
    url(r'^music/$', views.Music.as_view(), name='music'),
    #music/21/
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'album/add/$',views.AlbumCreate.as_view(),name="album-add"),
    #album/6/
    url(r'album/(?P<pk>[0-9]+)/$',views.AlbumUpdate.as_view(),name="album-update"),
    #album/6/delete
    url(r'album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name="album-delete"),
]