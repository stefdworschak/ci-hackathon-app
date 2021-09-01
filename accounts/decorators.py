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


def can_access_hackathon(view_type=None, redirect_url=None,
                         redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            hackathon = get_object_or_404(Hackathon,
                                          id=kwargs.get('hackathon_id'))
            is_default_org = hackathon.organisation.id == 1
            is_user_org = hackathon.organisation == request.user.organisation
            display_default_org = request.user.organisation.display_default_org
            is_public = hackathon.visibility == 'public'
            is_internal = hackathon.visibility == 'internal'
            user_is_default_org = request.user.organisation.id == 1
            is_created_by_user = hackathon.created_by == request.user
            is_staff_admin = request.user.user_type in [
                UserType.SUPERUSER, UserType.STAFF]
            is_hidden = (hackathon.status == 'deleted' or (
                hackathon.status == 'draft' and not is_created_by_user))

            if (is_hidden and not is_staff_admin):
                messages.error(request,
                               "You don't have access to this hackathon")
                return redirect(reverse(redirect_url))
            elif (view_type == 'admin' and
                    not hackathon.user_has_admin_access(request.user)):
                messages.error(request,
                               "You don't have access to this hackathon")
                return redirect(reverse(redirect_url))
            elif (view_type == 'judge' and
                    not hackathon.user_has_judge_access(request.user)):
                messages.error(request,
                               "You don't have access to this hackathon")
                return redirect(reverse(redirect_url))
            elif (view_type == 'facilitator' and
                    not hackathon.user_has_facilitator_access(request.user)):
                messages.error(request,
                               "You don't have access to this hackathon")
                return redirect(reverse(redirect_url))
            elif (is_public or ((display_default_org and is_default_org)
                                or is_user_org) or is_created_by_user
                    or (is_internal and user_is_default_org)):
                return view_function(request, *args, **kwargs)
            else:
                messages.error(request,
                               "You don't have access to this hackathon")
                return redirect(reverse('hackathon:hackathon-list'))

        return wrapped_view

    return decorator
