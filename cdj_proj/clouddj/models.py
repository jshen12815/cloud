from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#class Post(Comment):
 #   photo = models.ImageField(upload_to="album-art", default='album-art/randompic.jpg')
  #  song = models.FileField(upload_to="music")
   # plays = models.IntegerField(default = 0)
   # genre = models.CharField(max_length = 255)
  #  
   # def __unicode__(self):
    #    return self.profile +": "+self.text


#class Rating()


# Post-music file,album art,rating (as foreign key in Rate),comments(as foreign key in Comment),number of plays,genre



class Profile(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")

    def __unicode__(self):
         return self.user.username

#class Hashtag(models.Model): 
 #   text = models.CharField()

class Post(models.Model):
    profile = models.ForeignKey(Profile)
    text = models.CharField(max_length = 255)
  #  date = models.DateTimeField(auto_add_now=True)
    photo = models.ImageField(upload_to='album-art', default='album-art/randompic.jpg')
    song = models.FileField(upload_to="music")
    plays = models.IntegerField(default = 0)
    genre = models.CharField(max_length = 255)
#    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    
    def __unicode__(self):
        return self.profile.user.username +": "+self.text


class Comment(models.Model):
    profile = models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    text = models.CharField(max_length=200)
 #   date = models.DateTimeField(auto_add_now=true)
    
    def __unicode__(self):
        return self.text

#Rate -user(foreign key),#stars/discs/thumbs ups/clouds

class Rating(models.Model):
    profile= models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
   # rating = models.IntegerField(min_value=1, max_value=5)



class Playlist(models.Model):
    posts = models.ManyToManyField(Post, related_name="playlist")
    profile = models.ForeignKey(Profile)

