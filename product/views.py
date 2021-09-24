from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.views.generic import UpdateView

from rest_framework import viewsets, generics, status, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permissions import IsPostAuthor, IsAuthor, IsAuthorOrIsAdmin
from product.models import Category, Post, PostImage, Comment, Like, Favorite
from product.serializers import CategorySerializer, PostSerialzier, PostImageSerialzier, CommentSerializer, \
    FavoritePostSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]



class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialzier
    permission_classes = [IsAuthenticated,]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        """переопределим данный метод"""
        if self.action in ['update','partial_update','destroy']:
            permissions = [IsPostAuthor, ]
        else:
            permissions = [IsAuthenticated,]
        return [permission() for permission in permissions]

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'нравится' if like.is_liked else 'ненравится'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'нравится'
        return Response(message, status=200)

    def get_permission(self):
        if self.action == 'create' or self.action == 'like':
            return [IsAuthenticated()]
        return [IsAuthorOrIsAdmin()]

# --------------------------------------------------------------------------------------------------------
    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(post=post, user=user)
            favorite.is_favorite = not favorite.is_favorite
            if favorite.is_favorite:
                favorite.save()
            else:
                favorite.delete()
            message = 'В избранных' if favorite.is_favorite else 'Удалено из избранных'
        except Favorite.DoesNotExist:
            Favorite.objects.create(post=post, user=user, is_favorite=True)
            message = 'Добавлено в избранные'
        return Response(message, status=200)

        def get_permission(self):
            if self.action == 'create' or self.action == 'like' or self.action == 'favorite':
                return [IsAuthenticated()]
            return [IsAuthorOrIsAdmin()]
# --------------------------------------------------------------------------------------------------------



    """Фильтрацию по дате добавления """
    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('day', 0))
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(weeks=weeks_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

    """Фильтрация постов по имени создавшего"""
    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serialzier = PostSerialzier(queryset, many=True, context={'request':request})
        return Response(serialzier.data, status=status.HTTP_200_OK)

    """Создаем метод query params поисковик
    декоратор action работает только с ModelViewSet"""
    @action(detail=False, methods=['get'])    # указываем каким методом будет доступен этот  action
    def search(self, request, pk=None):
        q = request.query_params.get('q')       # query_params то же самое что и request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q)|
                                   Q(text__icontains=q))    #icontains чтобы фильтр не был чувствителен к регистру
        """| это знак или т.е фильтруй по названию или по тексту"""
        serializer = PostSerialzier(queryset,many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerialzier

    def get_serializer_context(self):
        return {'request': self.request}


# ---------------------------------------------------------------------------------------------------------------------------------

class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}




class UpdateCommentView(UpdateView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class DeleteCommentView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class CommentVeiwSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]



class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoritePostSerializer
    permission_classes = [IsAuthenticated,IsAuthor]























