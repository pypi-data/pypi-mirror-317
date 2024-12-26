from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
    ListView,
    FormView,
)

from crimsonslate_portfolio.models import Media
from crimsonslate_portfolio.forms import (
    MediaSearchForm,
    MediaUploadForm,
)


class MediaDetailView(DetailView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    model = Media
    queryset = Media.objects.filter(is_hidden__exact=False)
    template_name = "portfolio/media/detail.html"

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class MediaUpdateView(LoginRequiredMixin, UpdateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    fields = ["source", "thumb", "title", "desc", "is_hidden"]
    http_method_names = ["get", "post"]
    model = Media
    template_name = "portfolio/media/edit.html"
    partial_name = "portfolio/media/_edit.html"
    login_url = reverse_lazy("portfolio login")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_name
        return super().request(*args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class MediaDeleteView(LoginRequiredMixin, DeleteView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE}
    http_method_names = ["get", "post"]
    model = Media
    success_url = reverse_lazy("portfolio profile")
    template_name = "portfolio/media/delete.html"
    partial_name = "portfolio/media/_edit.html"
    login_url = reverse_lazy("portfolio login")

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.template_name = self.partial_name
        return super().request(*args, **kwargs)

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["title"] = self.get_object().title
        return context


class ContactView(TemplateView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Contact"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/contact.html"


class GalleryView(ListView):
    content_type = "text/html"
    context_object_name = "medias"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Gallery"}
    http_method_names = ["get", "post"]
    model = Media
    ordering = "-date_created"
    paginate_by = 12
    queryset = Media.objects.filter(is_hidden__exact=False)
    template_name = "portfolio/gallery.html"


class SearchView(FormView):
    allow_empty = True
    context_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Search"}
    http_method_names = ["get", "post"]
    template_name = "portfolio/search.html"
    partial_name = "portfolio/search_results.html"
    form_class = MediaSearchForm

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.headers.get("HX-Request"):
            self.__setattr__("template_name", self.partial_name)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: MediaSearchForm) -> HttpResponse:
        results: QuerySet = self.search_media(form)
        context: dict[str, Any] = self.get_context_data(results)
        return self.render_to_response(context)

    def get_context_data(
        self, results: QuerySet | None = None, **kwargs
    ) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["search_results"] = results
        return context

    def search_media(self, form: MediaSearchForm) -> QuerySet:
        results = Media.objects.filter(is_hidden=False)
        if form.cleaned_data["title"] != "*":
            results = results.filter(
                Q(title__contains=form.cleaned_data["title"])
                | Q(title__iexact=form.cleaned_data["title"])
            )
        return results


class UploadView(LoginRequiredMixin, FormView):
    content_type = "text/html"
    extra_context = {"profile": settings.PORTFOLIO_PROFILE, "title": "Upload"}
    form_class = MediaUploadForm
    http_method_names = ["get", "post"]
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("portfolio gallery")
    template_name = "portfolio/upload.html"

    def get_success_url(self, media: Media | None = None) -> str:
        if media is not None:
            return reverse("media detail", kwargs={"slug": media.slug})
        return reverse("portfolio gallery")

    def form_valid(self, form: MediaUploadForm) -> HttpResponseRedirect:
        media = Media.objects.create(
            source=form.cleaned_data["source"],
            thumb=form.cleaned_data["thumb"],
            title=form.cleaned_data["title"],
            subtitle=form.cleaned_data["subtitle"],
            desc=form.cleaned_data["desc"],
        )
        return HttpResponseRedirect(self.get_success_url(media))
