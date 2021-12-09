from django import forms

from django.db.models.base import Model

from .models import PdfForms
class PdfFormsform( forms.ModelForm):
    class Meta:
        model = PdfForms
        fields = ('job_Description',)
    