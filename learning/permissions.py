from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для администраторов - полный доступ, остальные - только чтение"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение для владельца - полный доступ, остальные - только чтение"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Проверяем владельца в зависимости от типа объекта
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_admin
        elif hasattr(obj, 'section'):
            return obj.section.owner == request.user or request.user.is_admin
        elif hasattr(obj, 'material'):
            return obj.material.section.owner == request.user or request.user.is_admin
        
        return request.user.is_admin


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Разрешение для преподавателей - создание и редактирование, студенты - только чтение"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_teacher


class IsStudentOrOwner(permissions.BasePermission):
    """Разрешение для студентов - прохождение тестов, владельцы - просмотр результатов"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Студенты могут проходить тесты
        if request.method == 'POST' and hasattr(obj, 'test'):
            return request.user.is_authenticated
        
        # Владельцы могут видеть результаты своих тестов
        if hasattr(obj, 'test') and hasattr(obj.test, 'material'):
            return obj.test.material.section.owner == request.user or request.user.is_admin
        
        return request.user.is_admin
