from rest_framework.permissions import IsAuthenticated, BasePermission

SAFE_METHODS = ['GET', ]


class IsOwnerAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        is_authenticated = super(
            IsOwnerAuthenticated,
            self).has_permission(
            request,
            view)
        return is_authenticated and view.get_object().owned_by == request.user


class IsCreatorAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        is_authenticated = super(
            IsCreatorAuthenticated,
            self).has_permission(
            request,
            view)
        return is_authenticated and view.get_object().created_by == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        elif view.action in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if view.action in ['list', 'retrieve']:
            return True

        # if not list or retrieve, if not log in then always False
        if not request.user.is_authenticated:
            return False
        return obj.owned_by == request.user


class IsReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):

        return (
            request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True

        # if not list or retrieve, if not log in then always False
        return False
