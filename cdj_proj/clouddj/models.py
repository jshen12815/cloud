from django.db import models

# Create your models here.
class Post(Comment):
    photo = models.ImageField(upload_to="album-art", default='album-art/randompic.jpg')
    song = models.FileField(upload_to=”music”)
    plays = models.IntegerField(default = 0)
    genre = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.profile +”: ”+self.text


class Rating()