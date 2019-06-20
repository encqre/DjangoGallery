from django.db import models
from datetime import datetime

class ImageCategory(models.Model):
    category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.category


class Image(models.Model):
    image_picture = models.ImageField(upload_to = 'gallery/static/gallery/pictures/', default = 'gallery/static/gallery/pictures/default/no-img.jpg')
    image_added = models.DateTimeField("date added", default=datetime.now())
    image_description = models.CharField(max_length=200)
    image_slug = models.CharField(max_length=200)
    image_visible = models.BooleanField(default=False)
    image_title = models.CharField(max_length=200)
    image_category = models.ForeignKey(ImageCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)

    def image_url(self):
        return str(self.image_picture.name).lstrip("gallery")

    def __str__(self):
        return self.image_title