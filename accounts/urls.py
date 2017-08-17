from django.conf.urls import url
from accounts import views

#index
urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^user/(?P<username>[a-z]+)/$', views.other_map , name="other_map"),
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
	url(r'^friend/(?P<pk>\d+)/block_cancle/$', views.block_cancle, name="block_cancle"),
    url(r'^friend_add/(?P<pk>\d+)$', views.friend_accept, name="friend_add"),
    url(r'^friend_reject/(?P<pk>\d+)$', views.friend_reject, name="friend_reject"),
    url(r'^friend_cancel/(?P<pk>\d+)$', views.friend_cancel, name="friend_cancel"),
]

#회원정보 수정
urlpatterns += [
	url(r'^setup_auth/$', views.setup_auth, name="setup_auth"),
	url(r'^preference/$', views.preference, name="preference"),
	url(r'^preference_design/$', views.preference_design, name="preference_design"),
	url(r'^preference_security/$', views.preference_security, name="preference_security"),
	url(r'^sign_out/(?P<pk>\d+)?$', views.sign_out, name="sign_out"),
]