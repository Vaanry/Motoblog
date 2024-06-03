from django import forms
from .models import Post, Comments, Location


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'description')
