from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing posts."""
    class Meta:
        model = Post
        fields = ['title', 'content']  # Do not include 'slug'


class CommentForm(forms.ModelForm):
    """Form for adding comments."""
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        label='',
    )

    class Meta:
        model = Comment
        fields = ['content']
