from django.urls import path
from . import views

urlpatterns = [
    path('', views.ratings_list, name='ratings'),
    path('search', views.search_form, name='search_form'),
    path('album/<str:uri>/', views.album_detail, name='album_detail'),
    path('rating/<int:ratingID>/', views.rating_detail, name='rating_detail'), # Rating by ID
    path('rating/<int:ratingID>/edit', views.rating_edit, name='rating_edit'), # Rating by Album?
    path('rating/<str:uri>/', views.rating_edit, name='rating_edit')
]