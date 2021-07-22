from functools import wraps

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse, redirect, get_object_or_404

from accounts.models import UserType
from hackathon.models import Hackathon


def can_access(allowed_types, redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            authorized = (request.user.user_type in allowed_types
                          or request.user.user_type is UserType.SUPERUSER)

            if not authorized and redirect_url:
                messages.error(request, 'You do not have access to this page!')
                return redirect(reverse(redirect_url, kwargs=redirect_kwargs))
            elif not authorized:
                raise PermissionDenied('You do not have access to this page!')

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator


def can_access_hackathon(redirect_url=None, redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):

            hackathon = get_object_or_404(Hackathon,
                                          id=kwargs.get('hackathon_id'))
            is_code_institute = hackathon.organisation.id == 1
            is_user_org = hackathon.organisation == request.user.organisation
            is_public = hackathon.is_public
            is_created_by_user = (hackathon.created_by
                                  == request.user.organisation)

            if not is_code_institute and not is_user_org:
                if not is_public and not is_created_by_user:
                    messages.error(request,
                                   "You don't have access to this hackathon")
                    return redirect(reverse('hackathon:hackathon-list'))

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator
