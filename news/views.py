from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def news_list(request,
	template='news/news_list.html'):

	post_list = Post.objects.all()
	

	if request.GET.get('real', None):
		template='news/news_list2.html'

	#페이지 네이션 구현 시작 
	paginator = Paginator(post_list, 3)
	page_num = request.POST.get('page')

	try:
		posts= paginator.page(page_num)
	except PageNotAnInteger:
		posts= paginator.page(1)
	except EmptyPage:
		posts=paginator.page(paginator.num_page)

	context = {'post_list':posts}
	if request.is_ajax():
		if request.POST.get('page',None):
			template = 'news/new_page_ajax.html'
			return render(request, template, context)
	#페이지 네이션 구현 끝

	return render(request, template, context)

def modal(request):
	pk = request.POST.get('pk', None)
	post = get_object_or_404(Post, pk=pk)
	print("되니")
	return render(request, 'news/post_modal.html',{
		'post':post,
		})

def post_destroy(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/news_list')