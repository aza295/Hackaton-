from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("Permission ", request.user.is_authenticated and request.user == obj.author)
        return request.user.is_authenticated and request.user == obj.author


# -----------------------------------------------------------------------------------------------------------------------------------

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user == obj.user)














class IsAuthorOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        """Срабатывает при действиях, в которых не нужен конкретный объект
        list and create.
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


    def has_object_permission(self, request, view, obj):
        """Срабатывает при действиях, в которых используется
        один конкретный объект: retrieve, update, delete
         всегда срабатывает после метода  has_permissions
         """
        if request.method in SAFE_METHODS: #
            return True
        return request.user and (request.user == obj.user or request.user.is_staff)