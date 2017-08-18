from django.conf.urls import url
from news import views

urlpatterns = [
	url(r'^$', views.news_list, name="news_list"),
	url(r'^(?P<pk>\d+)/destroy/$', views.post_destroy, name="post_destroy"),
]

#ajax전용 view
urlpatterns +=[
	#new_list modal
	url(r'^modal/$', views.modal, name="modal"),
	#modal 댓글 더보기
	url(r'^more/$', views.comment_more, name="comment_more"),
	#post 좋아요
	url(r'^like/$', views.news_like, name='post_like'),
	
]