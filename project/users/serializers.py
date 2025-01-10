from rest_framework import serializers
from django.contrib.auth import get_user_model


from .models import Author, Article

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','is_superuser','is_staff')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


#----------------------------------------------------------------

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'user','name', 'bio']

class ArticleSerializer(serializers.ModelSerializer):
    #author = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()) 

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']


class ArticleListSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Article
        fields = ['id', 'title']