from blog.models import Post, Comments
from motobikes.models import Motobike
from .serializers import (PostSerializer, MotoUserSerializer,
                          MotobikeSerializer, CommentsSerializer)
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .permissions import AuthorOrReadOnly, ReadOnly
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
       
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MotoViewSet(viewsets.ModelViewSet):
    queryset = Motobike.objects.all()
    serializer_class = MotobikeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 
    throttle_classes = (AnonRateThrottle,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('manufacturer', 'model')
    search_fields = ('manufacturer', 'model')


class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = MotoUserSerializer


class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (ReadOnly,)

    def get_queryset(self):
        comments = Comments.objects.filter(post__id=self.kwargs.get('post_id'))
        return comments


class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        comments = Comments.objects.filter(post__id=self.kwargs.get('post_id'))
        return comments
