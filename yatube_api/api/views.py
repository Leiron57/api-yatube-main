"""Представления API."""

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Comment, Group
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создание поста."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновление поста."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого поста запрещено!')
        serializer.save()

    def perform_destroy(self, instance):
        """Удаление поста."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого поста запрещено!')
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями."""

    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Получение комментариев поста."""
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        """Создание комментария."""
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_id']
        )

    def perform_update(self, serializer):
        """Обновление комментария."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение чужого комментария запрещено!'
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Удаление комментария."""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление чужого комментария запрещено!'
            )
        instance.delete()
