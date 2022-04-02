from django.urls import path, include
from . import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter

app_name = "gallery"

router = DefaultRouter()
router.register(r'users', views.ApiUserViewSet, basename="users")

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('gallery/<category_slug>', views.category_slug, name="category_slug"),
    path('gallery/', views.gallery, name="gallery"),
    path("id/<str:pk>", views.image, name="image"),
    path('about/', views.about, name="about"),
    path('api/', views.api, name="api"),
    path('api/swagger/', get_swagger_view(title="API documentation")),
    path('api/v1/images/', views.ApiImageList.as_view(), name="api_image_list"),
    path('api/v1/images/<str:pk>/', views.ApiImageDetail.as_view(), name="api_image"),
    path('api/v1/categories/', views.api_category_list, name="api_category_list"),
    path('api/v1/categories/<category_slug>/', views.api_category, name="api_category"),
    # path('api/v1/users/', views.ApiUserViewSet.as_view({'get': 'list'})),
    # path('api/v1/users/<int:pk>/', views.ApiUserViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/', include(router.urls)),
]