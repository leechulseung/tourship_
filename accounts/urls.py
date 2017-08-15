from django.conf.urls import url
from accounts import views

#index 
urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^preference/$', views.preference, name="preference"),
]

#로그인 전 url
urlpatterns += [
	url(r'^joinus/$', views.joinus, name="joinus"),
	
]

#친구
urlpatterns += [
	url(r'^friend/$', views.friend_list, name="friend_list"),
	url(r'^friend/favorites/$', views.friend_favorites, name="friend_favorites"),
	url(r'^friend/block_list/$', views.block_list, name="block_list"),
]