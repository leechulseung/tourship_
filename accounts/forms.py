from news.models import Post, Address, Comment, Photo, Postprivacy, Bookingpost
from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

from .models import Profile
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.shortcuts import redirect

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
	address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'주소를 입력하세요.'}),required=True)
	main_photo = forms.ImageField(required=True)
	def __init__(self, user=False, *args, **kwargs):
		self.user = user
		super().__init__(*args,**kwargs)

	class Meta:
		model = Post
		fields = ['title','tourday','content','privacy','main_photo','location']
		today = timezone.now()
		widgets={
		'title': forms.TextInput(attrs={'class':'form-control','placeholder':'제목을 입력하세요.'}),
        'tourday': DateInput(attrs={'class':'form-control','value':today.strftime("%Y-%m-%d")}),
        'content': forms.Textarea(attrs={'class':'form-control mt-2','placeholder':'내용을 입력하세요.'}),
        'privacy': forms.Select(attrs={'class':'form-control'}),
        'location': forms.HiddenInput(attrs={'id':'getLatgetLng','value':''}),
        }

	def save(self, commit=True):
		post = super().save(commit=commit)
		post.author = self.user
		post.save()
		addr = self.cleaned_data['address']
		address = Address.objects.create(post=post, address=addr)
		print("세이브")
		return post


class CheckForm(forms.Form):
	username = forms.CharField(widget=
		forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'email@tourpin.com',
			}))

	password = forms.CharField(widget=
		forms.PasswordInput(attrs={
			'class':'form-control',
			}))

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super().__init__(*args, **kwargs)

	def clean_username(self):
		username = self.cleaned_data['username']
		if not username == self.user.username:
			raise forms.ValidationError("아이디가 틀렸습니다.")
		return username

	def clean_password(self):
		password = self.cleaned_data["password"]
		if not self.user.check_password(password):
			raise forms.ValidationError("비밀번호가 틀립니다.")
		return password

class SetupForm(forms.Form):
	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(SetupForm, self).__init__(*args, **kwargs)

	newPassword1 = forms.CharField(
		label = '새로운 비밀번호',
		widget = forms.PasswordInput(attrs={
			'class':'form-control',
			}), required=False,
		)
	newPassword2 = forms.CharField(
		label = '새로운 비밀번호(확인용)',
		widget = forms.PasswordInput(attrs={
			'class':'form-control'
			}), required=False,
		)
	address = forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control'
		}), required=False,
	)
	phone_num= forms.CharField(validators=[RegexValidator(r'^010[1-9]\d{7}$')],max_length=11, widget= forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'01012345678'
        }),required=False,)

	photo = forms.ImageField(widget=forms.FileInput(
		attrs={'class':'form-control-file',}
		),
		required=False
	)




	def clean(self):
		password1 = self.cleaned_data.get('newPassword1')
		password2 = self.cleaned_data.get('newPassword2')
		address = self.cleaned_data.get('address')
		phone_num = self.cleaned_data.get('phone_num')
		photo = self.cleaned_data.get('photo')

		if not password1:
			if not password2:
				if not address:
					if not phone_num:
						if not photo:
							raise forms.ValidationError("")


	def clean_newPassword2(self):

		password1 = self.cleaned_data.get('newPassword1')
		password2 = self.cleaned_data.get('newPassword2')

		if password1 and password2:
			password1_isalpha = password1[0].isalpha()
			if password1 != password2:
				raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")
			if len(password1) < 8:
				raise forms.ValidationError("비밀번호가 짧습니다. 최소 8글자 이상 입력해 주세요(영문+숫자)")
			if all(c.isalpha() == password1_isalpha for c in password1):
				raise forms.ValidationError("비밀번호는 영문과 숫자 조합으로 다시 입력해 주세요.")
		if password2:
			if not password1:
				raise forms.ValidationError("비밀번호를 입력해주세요")
		if password1:
			if not password2:
				raise forms.ValidationError("비밀번호 확인을 입력해주세요")
		return password2



	def save(self, commit=True):
		if self.cleaned_data["newPassword2"]:
			password = self.cleaned_data["newPassword2"]
			self.user.set_password(password)
			if commit:
				self.user.save()

		if self.cleaned_data['address']:
			self.user.profile.address = self.cleaned_data['address']
			if commit:
				self.user.profile.save()

		if self.cleaned_data['phone_num']:
			self.user.profile.phone_num = self.cleaned_data['phone_num']
			if commit:
				self.user.profile.save()

		if self.cleaned_data['photo']:
			self.user.profile.photo = self.cleaned_data['photo']
			if commit:
				self.user.profile.save()

		return self.user

class Multi_PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']
        widgets = {
            'file' : forms.ClearableFileInput(attrs={'multiple': True})
        }


class BookingPostForm(forms.ModelForm):

	to_user= forms.EmailField(
		widget= forms.EmailInput(attrs={
		'class':'form-control',
		'placeholder':'계정명을 입력하세요.',
		}), required=False)

	class Meta:
		model = Bookingpost
		fields = ['title','content','location','address']
		today = timezone.now()
		
		widgets={
		'title': forms.TextInput(attrs={'class':'form-control','placeholder':'제목을 입력하세요.'}),
	    'content': forms.Textarea(attrs={'class':'form-control mt-2','placeholder':'내용을 입력하세요.'}),
	    'location': forms.HiddenInput(attrs={'id':'booking__hidden','value':''}),
	    'address': forms.TextInput(attrs={'id':'memoryBooking__address','class':'form-control', 'placeholder':'주소를 다시 받아오세요.'})
	    }

	def __init__(self, user=False, *args, **kwargs):
		self.user= user
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		print('세이브 접속')
		bpost = super().save(commit=commit)
		print("세이브 실행")
		bpost.from_user = self.user
		print("from유저에 요청유저넣기")
		to_user = self.cleaned_data.get('to_user', None)
		print(to_user,'투 유저 정보는 무엇일까요?')
		if to_user:
			bpost.to_user = User.objects.get(username= to_user)
		bpost.save()
		print("세이브완료")
		return bpost