
from django.db import models
from django.contrib.auth.models import User
import uuid


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='collections')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title


class CollectionMap(models.Model):
    collection_key = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='movies')
    movie_key = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('collection_key', 'movie_key')

    def __str__(self):
        return f"{self.collection_key.title} - {self.movie_key.title}"