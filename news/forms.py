from django import forms
from .models import Comment, Block_user, Report_Post

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

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block_user
        fields = ['reasons']
        widgets={
        'reasons': forms.TextInput(attrs={'class':'form-control'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report_Post
        fields = ['content']
        widgets={
        'content': forms.TextInput(attrs={'name':'report_content', 'class':'form-control '})
        }
