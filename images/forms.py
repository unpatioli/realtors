from django import forms

from images.models import ImagedItem

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImagedItem
        fields = ('image', 'title',)

