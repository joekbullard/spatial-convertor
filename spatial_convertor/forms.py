from django.forms import ModelForm
from django import forms
from .models import SpatialRecord


class RecordForm(ModelForm):
    upload_field = forms.FileField()

    class Meta:
        model = SpatialRecord
        fields = ["name"]
