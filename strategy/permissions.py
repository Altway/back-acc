from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only give the owner of the object access
    """
    message = 'You must be the owner of this object'

    def has_permission(self, request, view):
        if view.action == 'list' and not request.user.is_staff:
            print('has_permission false')
            print(request.headers)
            return True
        else:
            print('has_permission true')
            return True

    def has_object_permission(self, request, view, obj):
        print('enter has_object_permission')
        # only allow the owner to make changes
        user = self.get_user_for_obj(obj)
        print(f'user: {user.username}')
        if request.user.is_staff:
            print('has_object_permission true: staff')
            return True
        elif view.action == 'create':
            print('has_object_permission true: create')
            return True
        elif user == request.user:
            print('has_object_permission true: owner')
            return True # in practice, an editor will have a profile
        else:
            print('has_object_permission false')
            return False

    def get_user_for_obj(self, obj):
        model = type(obj)
        if model is models.UserProfile:
            return obj.user
        else:
            return obj.owner.user