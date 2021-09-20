from django.shortcuts import render
from rest_framework.views import APIView

"""Создаем вьюшки"""
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Responce ('Activation code was send', status = 200)
        return Responce(serializer.errors, status=400)