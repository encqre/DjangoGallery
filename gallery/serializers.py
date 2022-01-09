from rest_framework import serializers
from .models import Image, ImageCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCategory
        fields = ('name', 'slug')

class ImageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'title', 'category', 'date', 'url')


    def get_url(self, image):
        request = self.context.get('request')
        url = image.image.url
        return request.build_absolute_uri(url)