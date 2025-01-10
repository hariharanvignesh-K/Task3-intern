
from django.urls import path
from .views import RegisterView, LoginView, AuthorViewSet, ArticleViewSet
from rest_framework.urlpatterns import format_suffix_patterns

# Author Actions
author_list = AuthorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

author_detail = AuthorViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Article Actions
article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Author CRUD operations
    path('authors/', author_list, name='author-list'),
    path('authors/<int:pk>/', author_detail, name='author-detail'),

    # Article CRUD operations
    path('articles/', article_list, name='article-list'),
    path('articles/<int:pk>/', article_detail, name='article-detail'),
]

# Adding format suffix patterns (This is optional)
urlpatterns = format_suffix_patterns(urlpatterns)
