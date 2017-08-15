from news.models import Post, Address, Comment, Photo, Postprivacy
from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

GENDER_CHOICES = (
    ('남성','남성'),
    ('여성','여성'),
    )

POST_PRIVACY_CHOICES = ()

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


class SignUpForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.
		PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(widget=forms.
		PasswordInput(attrs={'class':'form-control'}))
	address = forms.CharField(widget=forms.TextInput(
		attrs = {'class':'form-control',}),
		required=False
	)
	birthdate = forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 'type':"date"}))
	gender = forms.ChoiceField(choices=GENDER_CHOICES,
		widget=forms.Select(attrs={
			'class':'form-control col-sm-4 col-md-3 col-lg-2',
			}))
	phone_num = forms.CharField(validators=[RegexValidator(r'^010[1-9]\d{7}$')], widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'01091833798',
		}),
		required=False
	)
	photo = forms.ImageField(widget=forms.FileInput(
		attrs={'class':'form-control-file',}
		),
		required=False
	)

	class Meta(UserCreationForm.Meta):
		fields = UserCreationForm.Meta.fields + ('first_name',)
		widgets = {
			'username':forms.EmailInput(attrs={
				'class':'form-control',
				'placeholder':'pilot@tourpin.com'
				}),
			'first_name':forms.TextInput(attrs={
				'class':'form-control',
				'placeholder':'이름을 입력해주세요.'
				}),
		}

	def clean_birthdate(self):
		birthdate = self.cleaned_data.get('birthdate')
		if birthdate:
			if birthdate.isalpha():
				raise forms.ValidationError("날짜 형식으로 다시 입력하세요. ")
		return birthdate

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')
		if first_name:
			if not first_name.isalpha():
				raise forms.ValidationError("이름형식으로 다시 입력하세요. ")
		if not first_name:
			raise forms.ValidationError("이름을 입력하세요")
		return first_name

	def save(self):
		user = super().save()
		profile = Profile.objects.create(user=user,
			phone_num = self.cleaned_data['phone_num'],
			address = self.cleaned_data['address'],
			gender = self.cleaned_data['gender'],
			birthdate = self.cleaned_data['birthdate'],
			photo = self.cleaned_data['photo'],
			)
		return user


class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
	address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'주소를 입력하세요.'}))
	photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'123','multiple': True}),required=False)

	class Meta:
		model = Post
		fields = ['title','tourday','content','privacy']
		today = timezone.now()
		widgets={
		'title': forms.TextInput(attrs={'class':'form-control','placeholder':'제목을 입력하세요.'}),
        'tourday': DateInput(attrs={'class':'form-control','value':today.strftime("%Y-%m-%d")}),
        'content': forms.Textarea(attrs={'class':'form-control mt-2','placeholder':'내용을 입력하세요.'}),
        'privacy': forms.Select(attrs={'class':'form-control'}),
        }

	def save(self):
		post = super().save()
		addr = self.cleaned_data['address']
		address = Address.objects.create(post=post, address=addr)
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

