from django.contrib import admin

from account.models import User

"""Регистрируем пользователя в админ панели"""
admin.site.register(User)