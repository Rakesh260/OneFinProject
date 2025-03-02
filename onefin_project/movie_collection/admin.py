from django.contrib import admin
from .models import Movie, Collection, CollectionMap


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'uuid', 'genres')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'uuid', 'user')


@admin.register(CollectionMap)
class CollectionMapAdmin(admin.ModelAdmin):
    list_display = ('collection_key', 'movie_key')
