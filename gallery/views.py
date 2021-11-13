from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Image, ImageCategory
from .serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
import uuid

#TODO display order, images per page and display columns should be saved in cookie to not mess from 

def api_image_list(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse('Only GET method is allowed for now')


def api_image(request, pk):
    try:
        image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return JsonResponse(serializer.data)
    else:
        return HttpResponse('Only GET method is allowed for now')


def image(request, pk):
    try:
        this_image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return HttpResponse(status=404)
    return redirect(this_image.image.url)
        

def homepage(request):
    return render(request=request, template_name='gallery/home.html')


def api(request):
    return render(request=request, template_name='gallery/api.html')


def random(request):
    return HttpResponse('Random pic here')


def gallery(request):
    order_by = request.GET.get('order')
    if order_by == "oldest":
        all_images = Image.objects.order_by('date')
    else:
        all_images = Image.objects.order_by('-date')
        order_by = "newest"
    these_categories = ImageCategory.objects.all()

    images_per_page = request.GET.get('images')
    if images_per_page == None:
        images_per_page = '25'

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
    
    display_format.update({"images_per_page": images_per_page})
    display_format.update({"order_by":order_by})
    display_format.update({"category":"All"})
    display_format.update({"total_images":str(len(all_images))})

    paginator = Paginator(all_images, int(images_per_page))

    page = request.GET.get('page')
    these_images = paginator.get_page(page)

    return render(request, 'gallery/gallery.html', {"images": these_images, "categories": these_categories, "display": display_format})


def category_slug(request, category_slug):
    category = ImageCategory.objects.filter(slug=category_slug)[0]
    order_by = request.GET.get('order')
    if order_by == "oldest":
        category_images = category.image_set.order_by('date')
    else:
        category_images = category.image_set.order_by('-date')
        order_by = "newest"
    these_categories = ImageCategory.objects.all()

    images_per_page = request.GET.get('images')
    if images_per_page == None:
        images_per_page = '25'

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
    
    display_format.update({"images_per_page": images_per_page})
    display_format.update({"order_by":order_by})
    display_format.update({"category":category.slug})
    display_format.update({"total_images":str(len(category_images))})

    paginator = Paginator(category_images, int(images_per_page))

    page = request.GET.get('page')
    these_images = paginator.get_page(page)

    return render(request, 'gallery/gallery.html', {"images": these_images, "categories": these_categories, "display": display_format})


def about(request):
    return HttpResponse('About')