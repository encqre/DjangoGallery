from django.contrib import admin
from .models import Image, ImageCategory
from django.db import models

admin.site.register(Image)
admin.site.register(ImageCategory)

# Register your models here.
