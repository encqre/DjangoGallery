from rest_framework import serializers
from .models import Image, ImageCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCategory
        fields = ('name', 'slug')

class ImageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Image
        fields = ('pk', 'title', 'url', 'date', 'category', 'uuid')