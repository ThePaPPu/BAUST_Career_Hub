from django import forms
from .models import Comment, Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('descriptions',)

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)