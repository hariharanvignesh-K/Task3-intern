from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer


from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework import viewsets
from .models import Author, Article
from .serializers import AuthorSerializer, ArticleSerializer, ArticleListSerializer



class RegisterView(APIView):                #Block for Register the new User 
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):                   #Block for Login the existing User
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:                #if user is available generate the Refersh Token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        




class AuthorViewSet(viewsets.ModelViewSet):         #Block for Author viewset which performs CRUD operations on it.
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):     #updation of author records, we use partial updation which means not all the fields are mandatory in request

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):    #This function is not mandatory , for verify the response msg.

        instance = self.get_object()  
        name = instance.name
        author_id = instance.id
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Author {name} id {author_id} has deleted successfully'
        })
    def perform_destroy(self, instance):

        instance.delete()

# Article ViewSet
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
                                                    # If the user is not authenticated, Give a limited contents of articles (only the title)
        if not self.request.user.is_authenticated:
            return ArticleListSerializer
        return ArticleSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_authenticated:
                                                    # Remove the content to 100 characters for unauthenticated users in the list view
            limited_articles = []
            for article in queryset:
                limited_content = article.content[:100] + '...' if len(article.content) > 100 else article.content
                limited_articles.append({
                    'id': article.id,
                    'title': article.title,
                    'content': limited_content
                })
            return Response(limited_articles)
        return super().list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        if not request.user.is_authenticated:
                                                # Show only first 100 characters to unauthenticated users
            limited_content = article.content[:100] + '...' if len(article.content) > 100 else article.content
            return Response({'title': article.title, 'content': limited_content})
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):         #same function has used in above

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):    #This is optional to verfy the response msg

        instance = self.get_object()  
        name = instance.title
        author_id = instance.id
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Title {name} "id" {author_id} has deleted successfully'
        })
    def perform_destroy(self, instance):

        instance.delete()