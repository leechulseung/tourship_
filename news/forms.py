from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets={
        'message': forms.TextInput(attrs={
        'class':"form-control mb-2 mr-sm-2 mb-sm-0 reply_text",
        'placeholder':'댓글을 입력해주세요.',    
            })
        }

        