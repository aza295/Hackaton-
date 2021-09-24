
from django.urls import path
from .views import RetrieveUpdateDestroyReviewView, CreateReviewView
urlpatterns = [
    path('review/', CreateReviewView.as_view()),
    path('review/<int:pk>/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/create/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/update/<int:pk>/', RetrieveUpdateDestroyReviewView.as_view()),
    path('review/delete/<int:pk>', RetrieveUpdateDestroyReviewView.as_view()),
]