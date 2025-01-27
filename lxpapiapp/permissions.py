from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'admin' as their utype
        return request.user.is_authenticated and request.user.is_superuser
    
class IsTrainer(permissions.BasePermission):
    """
    Custom permission to only allow users with 'Trainer' utype to access the view.
    """ 
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'Trainer' as their utype
        return request.user.is_authenticated and request.user.utype == '1'


class IsLearner(permissions.BasePermission):
    """
    Custom permission to only allow users with 'learner' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'learner' as their utype
        return request.user.is_authenticated and request.user.utype == '2'
    

class IsCTO(permissions.BasePermission):
    """
    Custom permission to only allow users with 'CTO' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'CTO' as their utype
        return request.user.is_authenticated and request.user.utype == '3'
    
class IsCFO(permissions.BasePermission):
    """
    Custom permission to only allow users with 'CFO' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'CFO' as their utype
        return request.user.is_authenticated and request.user.utype == '4'

class IsMentor(permissions.BasePermission):
    """
    Custom permission to only allow users with 'Mentor' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'Mentor' as their utype
        return request.user.is_authenticated and request.user.utype == '5'
    
class IsStaff(permissions.BasePermission):
    """
    Custom permission to only allow users with 'Staff' utype to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'Staff' as their utype
        return request.user.is_authenticated and request.user.utype == '6'
class IsAdminOrTrainer(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or Trainer.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '1')


class IsAdminOrLearner(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or Learner.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '2')


class IsAdminOrCTO(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or CTO.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '3')


class IsAdminOrCFO(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or CFO.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '4')


class IsAdminOrMentor(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or Mentor.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '5')


class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission to allow users who are either Admin or Staff.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.utype == '6')