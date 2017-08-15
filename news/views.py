from django.shortcuts import render, get_object_or_404
from .models import Post, Comment

def news_list(request, 
	template='news/news_list.html'):
	
	post_list = Post.objects.all()
	context = {'post_list':post_list}
	
	if request.GET.get('real', None):
		template='news/news_list2.html'
	return render(request, template, context)

def modal(request):
	pk = request.POST.get('pk', None)
	post = get_object_or_404(Post, pk=pk)
	print("되니")
	return render(request, 'news/post_modal.html',{
		'post':post,
		})
