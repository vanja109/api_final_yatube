from urllib import request
from posts.models import Comment, Follow, Group, Post
from rest_framework import permissions, viewsets
from .permissions import AuthorPermission
from django.shortcuts import get_object_or_404
from .pagination import PostsPagination

from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('group', 'author')
    serializer_class = PostSerializer
    permission_classes = (AuthorPermission, permissions.IsAuthenticatedOrReadOnly)
    #pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission, permissions.IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        post=get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post=post            
        )

    def get_queryset(self):
        post=get_object_or_404(Post, id=self.kwargs['post_id'])
        new_queryset = Comment.objects.filter(post=post)
        return new_queryset


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    #queryset = Follow.objects.select_related('user') #Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены.
    serializer_class = FollowSerializer
    permission_classes = (AuthorPermission, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user=get_object_or_404(Follow, user=self.request.user) #смотри сюда. попробуй по примеру коментов
        new_queryset = Comment.objects.filter(post=post)
        return new_queryset