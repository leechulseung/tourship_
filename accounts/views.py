from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm, Multi_PhotoForm
from news.models import Photo, Block_user
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

#friend
from friendship.models import Friend, FriendshipRequest

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

@login_required
def index(request): #게시글 등록
	forms = Multi_PhotoForm(request.POST, request.FILES)#다중사진
	post_list= request.user.post_set.all()
	locations= []
	for post in post_list:
		locations.append({'title':post.title, 'content':post.content,'post_id':post.id,'location':post.location})
		
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
	requests_uesr = Friend.objects.requests(request.user) #받은 리스트
	friendlist= Friend.objects.friends(request.user) #친구 리스트
	sent_requests = Friend.objects.sent_requests(request.user) #보낸 리스트		

	return render(request, 'friend/friend_list.html',{
		'requests_uesr':requests_uesr,
		'sent_requests':sent_requests,
		'friend_list':friendlist
		})

#친구 요청하기
@login_required
def friend_add(request,pk):
	user = get_user_model()
	if pk:
		to_user = user.objects.all().get(pk=pk)
		from_user = request.user
		Friend.objects.add_friend(from_user,to_user)
		return redirect('friend_list')

#즐겨찾기
@login_required
def friend_favorites(request):
	return render(request, 'friend/friend_favorites.html')

#차단 리스트
@login_required
def block_list(request):
	#block_cancle = request.GET.get('block_cancle', None) # 차단취소
	#if block_cancle:

	block_user = Block_user.objects.filter(author = request.user)
	print(block_user)
	return render(request, 'friend/block_list.html',{'block_list':block_user,})

def block_cancle(request,pk): #차단취소
    block = get_object_or_404(Block_user, pk=pk)
    block.delete()
    return redirect("/index/friend/block_list")

#친구 요청 허가
@login_required
def friend_accept(request,pk):
    f_request = get_object_or_404(FriendshipRequest, id=pk)
    f_request.accept()
    return redirect('friend_list')

#친구 요청 거절
@login_required
def friend_reject(request,pk):
    f_request = get_object_or_404(FriendshipRequest, id=pk)
    f_request.reject()
    return redirect('friend_list')

#친구 요청 취소
@login_required
def friend_cancel(request, pk):
    f_request = get_object_or_404(FriendshipRequest, id=pk)
    f_request.cancel()
    return redirect('friend_list')

#친구 삭제
@login_required
def friend_remove(request, pk):
	user_model = get_user_model()
	from_user = request.user
	to_user = user_model.objects.get(pk=pk)
	Friend.objects.remove_friend(from_user, to_user)
	return redirect('friend_list')

#다른 사람 여행지도 보기
@login_required
def other_map(request, username):
	if request.user.username == username:
		return redirect('index')
	user = get_user_model()
	try:
		user = user.objects.get(username= username)
	except user.DoesNotExist:
		return redirect('/')
	post_list= user.post_set.all()
	locations= []
	for post in post_list:
		locations.append({'title':post.title, 'content':post.content,'post_id':post.id,'location':post.location})
	requests_uesr = Friend.objects.requests(request.user) #받은 리스트
	friendlist= Friend.objects.friends(request.user) #친구 리스트
	sent_requests = Friend.objects.sent_requests(request.user) #보낸 리스트
	sent_requests_list=[u.to_user for u in sent_requests] #보낸 리스트 쿠킹

	return render(request, "friend/other_map.html",{
		'user_':user,
		'locations':locations,
		'friend_list':friendlist,
		'sent_requests':sent_requests_list,
		'requests':requests_uesr,
		})