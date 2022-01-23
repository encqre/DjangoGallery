from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Image, ImageCategory
from .serializers import ImageSerializer, CategorySerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

#TODO display order, images per page and display columns should be saved in cookie to not mess from 

class ApiImageList(generics.ListCreateAPIView):
    """
    Example of image upload:
    curl -X POST -S \
        -H "Content-Type: multipart/form-data" \
        -H "Accept: application/json" \
        -F "title=my image title" \
        -F "image=@/path/to/img/image.jpg;type=image/jpg" \
        http://localhost:8000/api/v1/images/

    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ApiImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# Using function based view approach
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def api_category_list(request):
    if request.method == 'GET':
        categories = ImageCategory.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse('Only GET and POST methods are allowed for now')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def api_category(request, category_slug):
    try:
        category = ImageCategory.objects.get(slug=category_slug)
    except ImageCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return HttpResponse('Only GET/PUT/DELETE methods are allowed')


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