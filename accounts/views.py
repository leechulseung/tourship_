from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm, Multi_PhotoForm
from news.models import Photo, Block_user
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.db.models import F,Q
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

#allauth
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

#Form
from .forms import LoginForm,SignUpForm,CheckForm,SetupForm
#Post
from news.models import Post

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
				'form':form,
				})
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
	page = request.GET.get('page')

	#추억삭제 & Pagination
	post_list = Post.objects.all().order_by('-id').filter(author=request.user)
	search = request.GET.get('search',"")

	#검색을 했을 경우
	if search:
		print("들어와라 얍")
		print(search)
		post_list = post_list.filter(Q(title__icontains=search) | Q(tourday__icontains=search))
		paginator = Paginator(post_list, 3)

		try:
			#현재 페이지 number와 앞,뒤 페이지 정보를 가짐
			post_list = paginator.page(page)
		except PageNotAnInteger:
			#page가 integer가 아니거나 없을 경우에는 첫 번째 페이지로 이동
			post_list = paginator.page(1)
		except EmptyPage:
			#범위를 넘는 큰 수를 입력 할 경우 마지막 페이지로 이동
			post_list = paginator.page(paginator.num_pages)
		return render(request,'accounts/index_search_modal.html',{'post_list':post_list, 'total_page':range(1, paginator.num_pages + 1)})

	paginator = Paginator(post_list, 3)

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

	try:
		#현재 페이지 number와 앞,뒤 페이지 정보를 가짐
		post_list = paginator.page(page)
	except PageNotAnInteger:
		#page가 integer가 아니거나 없을 경우에는 첫 번째 페이지로 이동
		post_list = paginator.page(1)
	except EmptyPage:
		#범위를 넘는 큰 수를 입력 할 경우 마지막 페이지로 이동
		post_list = paginator.page(paginator.num_pages)

	return render(request, 'accounts/index.html', {
		'form':form,
		'forms':forms,
		'locations':locations,
		'post_list':post_list,
		'current_page':page,
		'total_page':range(1, paginator.num_pages + 1),
		})

@login_required
def index_delete(request):
   if request.is_ajax():
      pk = request.POST.getlist('pk[]',None)
      for p in pk:
         post = Post.objects.get(pk=p)
         post.delete()
      message = {"message": "success"}
      return HttpResponse(json.dumps(message), content_type="application/json")
   message = {"message":"faild"}
   return HttpResponse('clear')


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


@login_required
def friend_list(request):
	return render(request, 'friend/friend_list.html')

@login_required
def friend_favorites(request):
	return render(request, 'friend/friend_favorites.html')

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