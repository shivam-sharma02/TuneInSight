from django.db import models

class UserPrediction(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    playlist = models.URLField()
    playlist_songs = models.JSONField()
    depressed = models.BooleanField(default=False)    
    sad_percentage = models.FloatField()
    happy_percentage = models.FloatField()
    calm_percentage = models.FloatField()
    energetic_percentage = models.FloatField()
    

    def __str__(self):
        return f"{self.username}'s Playlist"
