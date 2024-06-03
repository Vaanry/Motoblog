"""Serializers."""
from rest_framework import serializers
from blog.models import Post, Comments, Category, Location
from motobikes.models import Motobike
from django.contrib.auth import get_user_model

User = get_user_model()


class LocationSerializer(serializers.ModelSerializer):
    """LocationSerializer."""

    class Meta:
        """Meta."""

        model = Location
        fields = ('name', )


class CategorySerializer(serializers.ModelSerializer):
    """CategorySerializer."""

    class Meta:
        """."""

        model = Category
        fields = ('title', )


class MotobikeSerializer(serializers.ModelSerializer):
    """MotobikeSerializer."""

    class Meta:
        """."""

        model = Motobike
        fields = '__all__'


class MotoUserSerializer(serializers.ModelSerializer):
    motobike = MotobikeSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('username', 'motobike')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class PostSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    category = CategorySerializer()
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('title', 'text', 'author', 'pub_date', 'location', 'category')

    def create(self, validated_data):
        location = validated_data.pop('location')['name']
        category = validated_data.pop('category')['title']
        current_location = Location.objects.filter(name=location).first()
        current_category = Category.objects.filter(title=category).first()
        validated_data['location'] = current_location
        validated_data['category'] = current_category
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        location = validated_data.pop('location')['name']
        category = validated_data.pop('category')['title']
        instance.location = Location.objects.filter(name=location).first()
        instance.category = Category.objects.filter(title=category).first()
        instance.text = validated_data.get('text', instance.text)
        instance.title = validated_data.get('title', instance.title)
        instance.pk = validated_data.get('pk', instance.pk)
        instance.save()
        return instance


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('post', 'author', 'text')
