from django.urls import path
from .views import RegisterUserView, MovieListView, UserMovieCollection, CollectionDetailView, RequestCountView, \
    ResetRequestCountView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='fetch-all-movies'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('collection/', UserMovieCollection.as_view(), name='user-movie-collection'),
    path('collection/<uuid:collection_uuid>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset-request-count'),
]
