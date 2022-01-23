from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Image, ImageCategory


class UserSerializer(serializers.ModelSerializer):
    image_categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ImageCategory.objects.all()
    )
    images = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Image.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'image_categories', 'images']


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = ImageCategory
        fields = ('id', 'name', 'slug', 'created_by')


class ImageSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    # url = serializers.SerializerMethodField()
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Image
        # fields = ('id', 'title', 'category', 'date', 'url', 'image')
        fields = ('id', 'title', 'category', 'date', 'image', 'created_by')


    # def get_url(self, image):
    #     request = self.context.get('request')
    #     url = image.image.url
    #     return request.build_absolute_uri(url)