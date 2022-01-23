from django.db import models
from datetime import datetime
import uuid, os

class ImageCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        'auth.User', related_name='image_categories', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    #Rename uploaded picture to the ID
    def path_and_rename(self, filename):
        upload_to = 'images/'
        ext = filename.split('.')[-1]
        filename = f'{self.id}.{ext}'
        return os.path.join(upload_to, filename)
    
    image = models.ImageField(
        upload_to=path_and_rename, default='background-magic.jpg'
    )
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField("Date added", default=datetime.now())
    SFW = models.BooleanField(default=True)
    category = models.ManyToManyField(ImageCategory, verbose_name="Category")
    created_by = models.ForeignKey(
        'auth.User', related_name='images', on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.pk) + " - " + str(self.title)