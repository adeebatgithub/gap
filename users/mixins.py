from django import http
from django.contrib.auth.mixins import AccessMixin
from django.views.generic.edit import FormMixin as BaseFormMixin


class FormMixin(BaseFormMixin):
    """
    Form mixin with additional post method
    """

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GroupRequiredMixin(AccessMixin):
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if request.user.is_authenticated and request.user.is_member(self.group_name):
            return super().dispatch(request, *args, **kwargs)
        return http.HttpResponseForbidden()
