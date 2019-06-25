from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image, ImageCategory
from django.core.paginator import Paginator

def single_slug(request, single_slug):
    images = [p.image_slug for p in Image.objects.all()]
    if single_slug in images:
        this_image = Image.objects.get(image_slug = single_slug)
        picture_url = this_image.image_url()
        return render(request, 'gallery/image.html', {"image": this_image})
    else:
        return HttpResponse(f"{single_slug} is not an image yet.")

def homepage(request):
    return render(request=request, template_name='gallery/home.html')

def api(request):
    return render(request=request, template_name='gallery/api.html')

def random(request):
    return HttpResponse('Random pic here')

def gallery(request):
    all_images = Image.objects.all()
    these_categories = ImageCategory.objects.all()
    paginator = Paginator(all_images, 5) #5 images per page

    page = request.GET.get('page')
    these_images = paginator.get_page(page)
    return render(request, 'gallery/gallery.html', {"images": these_images, "categories": these_categories})

def category_slug(request, category_slug):
    return HttpResponse(f"{category_slug} is not a category. Yet.")

def about(request):
    return HttpResponse('About')