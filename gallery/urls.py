from django.urls import path, include
from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('gallery/<category_slug>', views.category_slug, name="category_slug"),
    path('gallery/', views.gallery, name="gallery"),
    path('api/', views.api, name="api"),
    path('api/random', views.random, name="random"),
    path("id/<int:pk>", views.image, name="image"),
    path('about/', views.about, name="about"),
    path('api/v1/images/', views.api_image_list, name="api_image_list"),
    path('api/v1/images/<int:pk>/', views.api_image, name="api_image"),
]