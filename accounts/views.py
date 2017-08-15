from django.shortcuts import render
from .forms import PostForm
from news.models import Photo
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse

#allauth
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

#Form
from .forms import LoginForm

import json

@user_passes_test(lambda user : not user.is_authenticated, login_url='index')
def login(request):
	providers = []
	user = get_user_model()
	state = {}

	for provider in get_providers():
		try:
			provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
		except SocialApp.DoesNotExist:
			provider.social_app = None
		providers.append(provider)

	if request.method == "POST":
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			auth_login(request,user)
			state['result'] = "success"
			return HttpResponse(json.dumps(state),
				content_type = "application/json")
		else:
			return render(request, 'accounts/login_modal_error.html',{
				'form':form,	})
	else:
		form = LoginForm(request)

	return render(request, 'accounts/login.html',{
		'providers':providers, 'form':form
		})

def index(request):
	if request.method == 'POST':
		form = PostForm(request.POST,request.FILES)
		if form.is_valid():
			post = form.save()
			Photo.objects.create(post=post, photo=form.cleaned_data['photo'])
	elif request.method == 'GET':
		form = PostForm()
	return render(request, 'accounts/index.html', {
		'form':form
		})


def joinus(request):

	return render(request, 'accounts/joinus.html')

def preference(request):
	return render(request, 'accounts/preference.html')

def friend_list(request):
	return render(request, 'friend/friend_list.html')

def friend_favorites(request):
	return render(request, 'friend/friend_favorites.html')

def block_list(request):
	return render(request, 'friend/block_list.html')