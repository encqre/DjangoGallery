from django.db import models
from datetime import datetime
import uuid, os

class ImageCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    #Rename uploaded picture to the UUID
    def path_and_rename(self, filename):
        upload_to = 'gallery/static/gallery/pictures/'
        ext = filename.split('.')[-1]
        if self.uuid:
            filename = '{}.{}'.format(self.uuid, ext)
        else:
            filename = '{}.{}'.format('fail', ext)
        return os.path.join(upload_to, filename)
    
    picture = models.ImageField(upload_to=path_and_rename, default='gallery/static/gallery/pictures/default/no-img.jpg')
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField("Date added", default=datetime.now())
    SFW = models.BooleanField(default=True)
    category = models.ManyToManyField(ImageCategory, verbose_name="Category")
    url = models.CharField(max_length=200, default='http://localhost:8000/id/1337')

    def image_url(self):
        return str(self.picture.name).lstrip("gallery")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.url = "http://localhost:8000/id/" + str(self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk) + " - " + str(self.title)