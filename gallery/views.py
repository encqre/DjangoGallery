from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image, ImageCategory
from django.core.paginator import Paginator

def single_slug(request, single_slug):
    images = [p.image_slug for p in Image.objects.all()]
    if single_slug in images:
        this_image = Image.objects.get(image_slug = single_slug)
        picture_url = this_image.image_url()
        image_data = open("gallery" + picture_url, "rb").read()
        if (picture_url.split(".")[-1] == "jpg") or (picture_url.split(".")[-1] == "jpeg") or (picture_url.split(".")[-1] == "jpe"):
            response = HttpResponse(image_data, content_type="image/jpeg")
            response['Content-Disposition'] = 'filename="' + this_image.image_title + '.jpg"'
            return response
        elif (picture_url.split(".")[-1] == "png"):
            response = HttpResponse(image_data, content_type="image/png")
            response['Content-Disposition'] = 'filename="' + this_image.image_title + '.png"'
            return response
        elif (picture_url.split(".")[-1] == "gif"):
            response = HttpResponse(image_data, content_type="image/gif")
            response['Content-Disposition'] = 'filename="' + this_image.image_title + '.gif"'
            return response
        else:
            return HttpResponse("Unknown image mimetype.")
    else:
        return HttpResponse(f"{single_slug} is not an image yet.")

def homepage(request):
    return render(request=request, template_name='gallery/home.html')

def api(request):
    return render(request=request, template_name='gallery/api.html')

def random(request):
    return HttpResponse('Random pic here')

def gallery(request):
    order_by = request.GET.get('order')
    if order_by == "oldest":
        all_images = Image.objects.order_by('image_added')
    else:
        all_images = Image.objects.order_by('-image_added')
        order_by = "newest"
    these_categories = ImageCategory.objects.all()

    pictures_per_page = request.GET.get('pictures')
    if pictures_per_page == None:
        pictures_per_page = '25'

    images_per_width = request.GET.get('display')
    if images_per_width == "1":
        display_format = {"col_style":"col-12", "width":"w-50", "display":"1"}
    elif images_per_width == "2":
        display_format = {"col_style":"col-6", "width":"w-100", "display":"2"}
    elif images_per_width == "3":
        display_format = {"col_style":"col-4", "width":"w-100", "display":"3"}
    elif images_per_width == "4":
        display_format = {"col_style":"col-3", "width":"w-100", "display":"4"}
    else:
        display_format = {"col_style":"col-6", "width":"w-100", "display":"2"}
    
    display_format.update({"pictures_per_page": pictures_per_page})
    display_format.update({"order_by":order_by})

    paginator = Paginator(all_images, int(pictures_per_page))

    page = request.GET.get('page')
    these_images = paginator.get_page(page)

    return render(request, 'gallery/gallery.html', {"images": these_images, "categories": these_categories, "display": display_format})

def category_slug(request, category_slug):
    return HttpResponse(f"{category_slug} is not a category. Yet.")

def about(request):
    return HttpResponse('About')