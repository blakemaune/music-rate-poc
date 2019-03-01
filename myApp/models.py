from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200, primary_key=True)
    art_url = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return str(self.name) + " by " + str(self.artist)

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + " rated " + str(self.album) + ": " + str(self.value)