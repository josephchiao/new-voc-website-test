from django import forms

from .models import Comment, TripReport
from trips.models import Trip

from django_quill.forms import QuillFormField
import json
from wagtail.rich_text import RichText

class TripReportForm(forms.ModelForm):
    class Meta:
        model = TripReport
        fields = ["title", "body", "trip"]

    def clean_body(self):
        body_data = self.cleaned_data.get("body")
        try:
            body_json = json.loads(body_data)
            body_html = body_json.get("html", "")
            return RichText(body_html)
        except (ValueError, KeyError, TypeError):
            raise forms.ValidationError("Invalid trip report body format")

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
        }),
    )
    trip = forms.ModelChoiceField(
        queryset=Trip.objects.all(),
        widget=forms.Select(attrs={"id": "trip-select"}),
        label="Trip (optional)",
        required=False
    )
    body = QuillFormField(label="Trip Report Content")  

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": ""
        }
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment..."})
        }