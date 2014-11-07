from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")

    def __unicode__(self):
         return self.user.username

class Hashtag(models.Model): 
    text = models.CharField(max_length=200)

class Post(models.Model):
    profile = models.ForeignKey(Profile)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='album-art', default='album-art/randompic.jpg')
    song = models.FileField(upload_to="music")
    plays = models.IntegerField(default=0)
    genre = models.CharField(max_length=255)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    
    def __unicode__(self):
        return self.profile.user.username +": "+self.text


class Comment(models.Model):
    profile = models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.text


class Rating(models.Model):
    profile= models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    rating = models.IntegerField()



class Playlist(models.Model):
    posts = models.ManyToManyField(Post, related_name="playlist")
    profile = models.ForeignKey(Profile)

