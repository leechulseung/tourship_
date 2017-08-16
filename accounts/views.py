from django.shortcuts import render,redirect
from .forms import PostForm, Multi_PhotoForm
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
from .forms import LoginForm,SignUpForm,CheckForm,SetupForm

import json

#사용자 인증 여부 리턴
from django.utils import timezone


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

def index(request): #게시글 등록
	forms = Multi_PhotoForm(request.POST, request.FILES)#다중사진
	user_list= request.user.post_set.all()
	locations = [c.location for c in user_list]
	print(locations)
	if request.method == 'POST':
		form = PostForm(request.user,request.POST,request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			if form.is_valid(): #다중사진
				files = request.FILES.getlist('file')# list형태로 입력받은 파일들을 files에 저장
				for f in files:#입력받은 리스트(사진) 순회
					Photo.objects.create(post=post, file=f)
				return redirect('index')
	elif request.method == 'GET':
		form = PostForm()

	return render(request, 'accounts/index.html', {
		'form':form,
		'forms':forms,
		'locations':locations,
		})


@user_passes_test(lambda user : not user.is_authenticated, login_url='index')
def joinus(request):
	form = SignUpForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		if request.FILES:
			fiels = request.FILES.get('photo',None)
		form.save()
		return redirect('login')
	return render(request, 'accounts/joinus.html',{
		'form':form
		})

@login_required
def setup_auth(request):
    if request.method == "POST":
        form = CheckForm(request.user, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_info =  authenticate(username=username, password=password)
            if user_info is not None:
            	time = timezone.now() + timezone.timedelta(seconds=200)
            	request.session['is_auth'] = json.dumps(time.strftime('%d%H%M%S'))
            	return redirect('preference')
    elif request.method == "GET":
        form = CheckForm(request.user)
    return render(request, 'accounts/preference0_reconfirm.html',{
        'form':form,
        })

@login_required
def preference(request):
	authtime = request.session.get('is_auth', None)
	if authtime is not None:
		timenow = timezone.now()
		timenow = json.dumps(timenow.strftime('%d%H%M%S'))
		if authtime < timenow:
			return redirect('setup_auth')
	if request.method == "POST":
		form = SetupForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	elif request.method == "GET":
		form = SetupForm(user=request.user, data=request.POST)
	return render(request, 'accounts/preference1_information_modification.html',{
		'form':form,
		})

@login_required
def preference_design(request):
	authtime = request.session.get('is_auth', None)
	if authtime is not None:
		timenow = timezone.now()
		timenow = json.dumps(timenow.strftime('%d%H%M%S'))
		if authtime < timenow:
			return redirect('setup_auth')
	return render(request, 'accounts/preference2_decoration.html')

@login_required
def preference_security(request):
	authtime = request.session.get('is_auth', None)
	if authtime is not None:
		timenow = timezone.now()
		timenow = json.dumps(timenow.strftime('%d%H%M%S'))
		if authtime < timenow:
			return redirect('setup_auth')
	return render(request, 'accounts/preference3_notification_&_security.html')


@login_required
def sign_out(request, pk):
	authtime = request.session.get('is_auth', None)
	if authtime is not None:
		timenow = timezone.now()
		timenow = json.dumps(timenow.strftime('%d%H%M%S'))
		if authtime < timenow:
			return redirect('setup_auth')
	if pk:
		user = request.user
		user.delete()
		return redirect('/')
	return render(request, 'accounts/preferencen4_withdrawl.html')



def friend_list(request):
	return render(request, 'friend/friend_list.html')

def friend_favorites(request):
	return render(request, 'friend/friend_favorites.html')

def block_list(request):
	return render(request, 'friend/block_list.html')