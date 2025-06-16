from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'input'}),
            'text': forms.Textarea(attrs={'placeholder': 'Your comment...', 'class': 'textarea'}),
        }
