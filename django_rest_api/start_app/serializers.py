from django.contrib.auth.models import User, Group
from .models import File, Deal, Article
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group

# For additional modules (не по ТЗ)
class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    body = serializers.CharField()
    author_id = serializers.IntegerField()
    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.save()
        return instance

class FileSerializer(serializers.Serializer):
    created = serializers.CharField(max_length=120)
    datafile = serializers.CharField()
    def create(self, validated_data):
        return File.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.created = validated_data.get('created', instance.created)
        instance.datafile = validated_data.get('datafile', instance.datafile)
        instance.save()
        return instance