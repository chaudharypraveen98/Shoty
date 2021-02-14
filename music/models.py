from django.db import models
from django.urls import reverse
from django import forms
from myfirstproject import settings
from django.core.files.storage import FileSystemStorage


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    album_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return (self.album_title + "-" + self.artist)


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, default="mp3")
    song_title = models.CharField(max_length=250)
    song_logo = models.ImageField(default='2.jpg')
    song_link = models.FileField(upload_to='', default='see.mp3')
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return (self.song_title)


class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=400)
    message = models.CharField(max_length=2500)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return (self.name)
