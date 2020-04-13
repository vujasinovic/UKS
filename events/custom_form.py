from django import forms
from uxhub.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issues']
        widgets = {
            'description': forms.Textarea({"rows": 5, "cols": 20}),
            'author': forms.HiddenInput()
        }


class CommentFormTest(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description', 'author', 'issues']
        widgets = {
            'description': forms.Textarea({"rows": 5, "cols": 20}),
            'author': forms.HiddenInput()
        }