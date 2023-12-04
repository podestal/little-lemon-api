from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.is_staff)
    
class IsAdminOrReadOnlyOrIsAnonymous(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return bool(request.user.is_anonymous or request.user.is_superuser)
        return bool(request.user and request.user.is_staff)
    

