from django.urls import path, include
from rest_framework.routers import SimpleRouter

from product.views import UpdateCommentView, DeleteCommentView, CreateCommentView, FavoriteListView


urlpatterns = [
path('comments/', CreateCommentView.as_view()),
path('comments/update/<int:pk>/', UpdateCommentView.as_view()),
path('comments/delete/<int:pk>/', DeleteCommentView.as_view()),
path('favorites/', FavoriteListView.as_view()),
]