from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Decorator to restrict access to unauthenticated users.

    This decorator is applied to views that should only be accessible
    to users who are not logged in. If a user is already authenticated,
    they are redirected to the 'home' page.

    Parameters:
    - view_func: The original view function.

    Returns:
    - HttpResponse: Redirects to 'home' if the user is authenticated,
      or calls the original view function.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allow_users(allowed_roles: list[str]):
    """
    Decorator to restrict access to specific user roles.

    This decorator is applied to views that should only be accessible
    to users with certain roles specified in the 'allowed_roles' list.
    Users with roles not in the list will receive an "unauthorized"
    message.

    Parameters:
    - allowed_roles (list[str]): A list of allowed user roles.

    Returns:
    - HttpResponse: Displays an "unauthorized" message or calls the
      original view function.
    """

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator


def admin_only(view_func):
    """
    Decorator to restrict access to admin users.

    This decorator is applied to views that should only be accessible
    to users with the 'admin' role. Users with the 'customer' role are
    redirected to the 'user' page, and users with other roles receive
    no response.

    Parameters:
    - view_func: The original view function.

    Returns:
    - HttpResponse: Redirects users with the 'customer' role to the 'user'
      page, or calls the original view function for users with the 'admin' role.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'customer':
                return redirect('user')
            if group == 'admin':
                return view_func(request, *args, **kwargs)

    return wrapper_func
