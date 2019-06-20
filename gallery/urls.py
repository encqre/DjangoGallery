from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('gallery/<category_slug>', views.category_slug, name="category_slug"),
    path('gallery/', views.gallery, name="gallery"),
    path('api/', views.api, name="api"),
    path('api/random', views.random, name="random"),
    path("id/<single_slug>", views.single_slug, name="single_slug"),
    path('about/', views.about, name="about"),
]