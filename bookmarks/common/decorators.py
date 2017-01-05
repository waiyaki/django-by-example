import functools

from django.http import HttpResponseBadRequest


def ajax_required(func):
    @functools.wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return func(request, *args, **kwargs)
    return wrapped
