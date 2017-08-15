from news.models import Post, Address, Comment, Photo, Postprivacy
from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
	address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'주소를 입력하세요.'}))
	photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'123','multiple': True}),required=False)

	class Meta:
		model = Post
		fields = ['title','tourday','content','privacy','location']
		today = timezone.now()
		widgets={
		'title': forms.TextInput(attrs={'class':'form-control','placeholder':'제목을 입력하세요.'}),
        'tourday': DateInput(attrs={'class':'form-control','value':today.strftime("%Y-%m-%d")}),
        'content': forms.Textarea(attrs={'class':'form-control mt-2','placeholder':'내용을 입력하세요.'}),
        'privacy': forms.Select(attrs={'class':'form-control'}),
        'location': forms.HiddenInput(attrs={'id':'getLatgetLng','value':''}),
        }

	def save(self):
		post = super().save()
		addr = self.cleaned_data['address']
		address = Address.objects.create(post=post, address=addr)
		print("세이브")
		return post

class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=
		forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'email@tourpin.com',
			}))

	password = forms.CharField(widget=
		forms.PasswordInput(attrs={
			'class':'form-control',
			}))
	def clean(self):
		username = self.cleaned_data.get('username',None)
		password = self.cleaned_data.get('password',None)

		if username is None:
			raise forms.ValidationError("ID/Email을 입력하지 않으셨습니다.")
		if password is None:
			raise forms.ValidationError("패스워드를 입력하지 않으셨습니다.")
		if username and password:
			self.user_cache = authenticate(username=username, password=password)
			if self.user_cache is None:
				raise forms.ValidationError("아이디 또는 비밀번호를 다시 확인하세요")

