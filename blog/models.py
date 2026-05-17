from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='image/', default='image/default.jpg')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.id})


class Music(models.Model):
    name = models.CharField(max_length=200)
    music = models.FileField(upload_to='music/', default='music/default.mp3')
    created = models.DateTimeField(auto_now_add=True)
    

    

    