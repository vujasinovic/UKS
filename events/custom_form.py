from django import forms

from uxhub.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description', 'users', 'issues']
        widgets = {
            'description': forms.Textarea({"rows": 5, "cols": 20})
        }

