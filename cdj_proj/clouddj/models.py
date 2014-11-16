from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="following")

    def __unicode__(self):
        return self.user.username


class Hashtag(models.Model): 
    text = models.CharField(max_length=200, primary_key=True)

    # number of posts with this hashtag in it
    def numPosts(self):
        return len(self.posts)


class Project(models.Model):
    profile = models.ForeignKey(Profile)
    status = models.CharField(max_length=255)  # in_progress vs. complete


class Song(models.Model):
    name = models.CharField(blank=True, max_length=30)
    file = models.FileField(upload_to="music")
    edit_number = models.IntegerField(default=0)
    project = models.ForeignKey(Project)


class Post(models.Model):
    profile = models.ForeignKey(Profile)
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255, default='')
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='album-art', default='album-art/default.jpg')
    song = models.OneToOneField(Song)
    plays = models.IntegerField(default=0)
    genre = models.CharField(max_length=255)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts')
    
    def __unicode__(self):
        return self.profile.user.username +": "+self.text

    @staticmethod
    def get_posts_containing(user, query):
        return Post.objects.filter(Q(text__contains=query) | Q(title__contains=query))

    @staticmethod
    def get_stream_posts(user):
        return reversed(Post.objects.all().filter(Q(profile__in=user.following.all()) | Q(profile=user)))

    # once the text is set, parse the hashtags from it and save them
    def setHashtags(self):
        newhts = set([i[1:] for i in line.split() if i.startswith("#")])
        curr = set([ht.text for ht in self.hashtags])

        # add new hashtags to old list
        for hashtag in newhts:
            if hashtag not in curr:
                if Hashtag.objects.filter(text=hashtag):
                    h = Hashtag.objects.get(text=hashtag)
                else:
                    h = Hashtag(text=hashtag)
                    h.save()

                self.hashtags.add(h)

        # remove hashtags from old list that aren't in new hashtags
        for hashtag in curr:
            if hashtag not in newhts:
                # we know that hashtag already exists
                h = Hashtag.objects.get(text=hashtag)
                self.hashtags.remove(h)

        self.save()


class Comment(models.Model):
    profile = models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.text


class Rating(models.Model):
    numratings = models.IntegerField(default=0)
    profile= models.ForeignKey(Profile)
    post = models.ForeignKey(Post)
    rating = models.IntegerField()


class Playlist(models.Model):
    posts = models.ManyToManyField(Post, related_name="playlist")
    profile = models.ForeignKey(Profile)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)