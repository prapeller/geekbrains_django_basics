from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views import View


class IsStuffDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(IsStuffDispatchMixin, self).dispatch(request, *args, **kwargs)


class IsSuperuserDispatchMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(IsSuperuserDispatchMixin, self).dispatch(request, *args, **kwargs)