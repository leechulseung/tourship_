from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Post, Comment, Block_user, Report_Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, BlockForm, ReportForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F,Q

import json

from friendship.models import Friend

@login_required
def news_list(request,
	template='news/news_list.html'):
	search = request.GET.get('search', None) #검색
	like_list = [user.post for user in request.user.like_set.all()]
	like_first = request.GET.get('like_first') #좋아요 순서
	block_form = BlockForm(request.POST) #차단 폼
	report_form = ReportForm(request.POST) #신고 폼
	report_id = request.POST.get('report_id', None) # 신고id
	post_list = Post.objects.all()

	if search:  #검색하기
		post_list = post_list.filter(title__icontains=search)

	if request.GET.get('real', None):
		template='news/news_list2.html'


	if like_first:
		post_list = Post.objects.order_by('-like')

	block = Block_user.objects.all() #차단 table객체
	blocker = block.filter(author=request.user) #차단한 유저
	post_list_real = [] #차단당하지 않은 나머지 유저들
	block_user = []	#차단당한 유저
	for i in blocker:
		block_user.append(i.block_man_id)
	for i in post_list:
		if i.author.username in block_user:
			pass
		else:
			post_list_real.append(i)

	if block_form.is_valid(): #차단하기
		block_name = request.POST.get('block_name', None) #차단당한 유저
		block_id = request.POST.get('block_id', None) #차단당한 유저
		block = block_form.save(commit=False)
		block.block_man = block_name
		block.block_man_id = block_id
		block.author = request.user
		block.save()
		return redirect('/newspeed')

	if report_form.is_valid(): #신고하기
		report_title = request.POST.get('report_title') # 신고 게시글제목
		#print(report_title)
		post = Post.objects.get(pk=report_title) #
		report = report_form.save(commit=False)
		report.user = report_id
		report.title = post
		report.save()
		return redirect('/newspeed')

	#페이지 네이션 구현 시작
	paginator = Paginator(post_list_real, 3) #3개씩 묶어 페이지 생성
	page_num = request.POST.get('page') #ajax로 page번호를 보낸다면 해당 변수에 대입

	try:
		posts= paginator.page(page_num) #해당 변수의 페이지를 posts변수에 넣어줌
	except PageNotAnInteger:
		posts= paginator.page(1) #위 상황에서 에러가 발생한다면 첫번쨰 페이지
	except EmptyPage:
		posts=paginator.page(paginator.num_page)

	if request.GET.get('real', None):
		friendlist= Friend.objects.friends(request.user) #친구 리스트
		lists=[]
		for list_object in posts:
			if list_object in friendlist:
				lists.append(list_object)
		template='news/news_list2.html'

	context = {
	'post_list':posts,
	'block_form':block_form,
	'report_form':report_form,
	'like_list':like_list,
	} #템플릿에 넘겨줄 변수

	if request.GET.get('real', None):
		lists = Post.objects.order_by('-created_at').filter(Q(author=request.user) | Q(author__friends__from_user=request.user) | Q(author__friends__to_user=request.user)).distinct()

		template='news/news_list2.html'
		context = {
		'post_list':lists,
		'block_form':block_form,
		'report_form':report_form,
		'like_list':like_list,
		} #템플릿에 넘겨줄 변수

	if request.is_ajax(): #만약 ajax로 왔을떄
		if request.POST.get('page',None): #page변수가 왔다면
			template = 'news/new_page_ajax.html' #해당 템플릿을
			return render(request, template, context) #렌더해 리턴해준다.
	#페이지 네이션 구현 끝



	return render(request, template, context)

#post모달 내용
@login_required
def modal(request, template='news/post_modal.html'):
	pk = request.POST.get('pk', None)
	post = get_object_or_404(Post, pk=pk)

	comments = Comment.objects.filter(post=post) #댓글들
	form = CommentForm(request.POST or None) #댓글 폼
	like_list = [user.post for user in request.user.like_set.all()]
	context = {'post':post,'form':form, 'comments':comments, 'like_list':like_list, }

	if request.POST.get('message', None):
		if form.is_valid():
			com= form.save(commit=False)
			com.author = request.user
			com.post = post
			com.save()
			template = 'news/comment_ajax.html'
			context = {'comment':com,}

	return render(request, template, context)

#댓글 더보기
@login_required
def comment_more(request):
	pk = request.POST.get('pk', None)
	post = get_object_or_404(Post, pk=pk)
	if request.is_ajax():
		comments = Comment.objects.filter(post=post)[4:]
		return render(request,'news/comment_more.html',{
            'comments':comments,
            })
	return redirect("news:news_list")

@login_required
def news_like(request):
    pk = request.POST.get('pk', None)
    print(pk)
    post = get_object_or_404(Post, pk=pk)
    # 중간자 모델 Like 를 사용하여, 현재 post와 request.user에 해당하는 Like 인스턴스를 가져온다.
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()
        message = "like_del"
    else:
        message = "like"

    context = {'like_count': post.like_count,
               'message': message,
               'username': request.user.first_name }

    return HttpResponse(json.dumps(context))

@login_required
def post_destroy(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("/newspeed")


