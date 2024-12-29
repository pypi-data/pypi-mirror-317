from django import http
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin

from .. import utils
from ..models import League, Preference, PickerMembership


class SimpleFormMixin(FormMixin):
    success_msg = None
    redirect_path = None

    def get_success_url(self):
        return self.redirect_path or self.request.path

    def form_valid(self, form):
        if self.success_msg:
            messages.success(self.request, self.success_msg)

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class SimplePickerViewBase(TemplateView):
    @staticmethod
    def redirect(name, *args, **kwargs):
        return http.HttpResponseRedirect(reverse(name, args=args, kwargs=kwargs))

    @property
    def season(self):
        season = self.kwargs.get("season")
        if season:
            return season

        league = self.league
        return league.current_season or league.latest_season

    @cached_property
    def leagues(self):
        return League.active.all()

    @cached_property
    def league(self):
        return get_object_or_404(League.active, slug=self.kwargs["league"])

    def get_template_names(self, template_override=None):
        if template_override is None and self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name', 'template_override' argument, or an implementation of "
                "'get_template_names()'"
            )

        self.template_names_list = utils.get_templates(
            template_override or self.template_name, self.league
        )
        return self.template_names_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        league = self.league
        data.update(
            {
                "now": timezone.now(),
                "league": league,
                "season": self.season or league.current_season,
                "league_base": loader.select_template(
                    [
                        "picker/{}/base.html".format(league.slug),
                        "picker/base.html",
                    ]
                ),
            }
        )
        return data

    def render_to_response(self, context, template_override=None, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        template_names = self.get_template_names(template_override=template_override)
        context["template_names"] = template_names
        return self.response_class(
            request=self.request,
            template=template_names,
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )


class PickerViewBase(LoginRequiredMixin, SimplePickerViewBase):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            preferences=Preference.objects.get(user=self.request.user),
            memberships=self.memberships,
            **kwargs,
        )

    @cached_property
    def memberships(self):
        return list(PickerMembership.active.for_user(self.request.user, league=self.league))
