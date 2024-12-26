from typing import Any
from django import forms
from django.forms import ModelForm, widgets
from django.urls import reverse_lazy

from crimsonslate_portfolio.models import Media


class MediaUploadForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
        ]


class MediaEditForm(ModelForm):
    class Meta:
        model = Media
        fields = [
            "source",
            "thumb",
            "title",
            "subtitle",
            "desc",
            "is_hidden",
            "categories",
            "date_created",
        ]


class MediaSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        widget=widgets.TextInput(
            attrs={
                "hx-trigger": "load, keyup changed delay:150ms",
                "hx-post": reverse_lazy("portfolio search"),
                "class": "w-full block rounded p-2 border-gray-600",
                "autofocus": True,
                "autocomplete": False,
            }
        ),
    )

    def clean_title(self) -> str:
        if not self.cleaned_data.get("title"):
            self.cleaned_data["title"] = "*"
        return self.cleaned_data["title"]
