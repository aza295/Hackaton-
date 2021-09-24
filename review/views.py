from django.db.models import Avg
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from product.permissions import IsAuthor
from .models import Review
from .serializers import CreateReviewSerializer


class CreateReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer


class RetrieveUpdateDestroyReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer




