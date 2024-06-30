from rest_framework import serializers
from posts.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['photo']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)

        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)

        for image_data in images_data:
            PostImage.objects.create(post=post, **image_data)

        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = instance.likes.count()
        return representation
