from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('group', 'author')
    serializer_class = PostSerializer
    permission_classes = (
        AuthorPermission, permissions.IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorPermission, permissions.IsAuthenticatedOrReadOnly
)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
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
    serializer_class = FollowSerializer
    permission_classes = (AuthorPermission, permissions.IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()
