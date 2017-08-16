from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test

import json

@login_required
def news_list(request,
	template='news/news_list.html'):

	post_list = Post.objects.all()
	if request.GET.get('real', None):
		template='news/news_list2.html'

	#페이지 네이션 구현 시작 
	paginator = Paginator(post_list, 3) #3개씩 묶어 페이지 생성
	page_num = request.POST.get('page') #ajax로 page번호를 보낸다면 해당 변수에 대입

	try:
		posts= paginator.page(page_num) #해당 변수의 페이지를 posts변수에 넣어줌
	except PageNotAnInteger:
		posts= paginator.page(1) #위 상황에서 에러가 발생한다면 첫번쨰 페이지
	except EmptyPage:
		posts=paginator.page(paginator.num_page) 

	context = {'post_list':posts} #템플릿에 넘겨줄 변수
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

	context = {'post':post,'form':form, 'comments':comments, }

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
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message': message,
               'username': request.user.first_name }

    return HttpResponse(json.dumps(context))

@login_required
def post_destroy(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/news_list')


