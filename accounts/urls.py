from django.conf.urls import url
from accounts import views

#index
urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^user/(?P<username>[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3})/$', views.other_map , name="other_map"),
	#tour_flag
	url(r'^tour_flag/$', views.tour_flag, name='tour_flag'),
]

#로그인 전 url
urlpatterns += [
	url(r'^joinus/$', views.joinus, name="joinus"),

]

#추억삭제
urlpatterns += [
   url(r'^delete/$', views.index_delete, name="delete"),
]

#친구
urlpatterns += [
	url(r'^friend/$', views.friend_list, name="friend_list"),
	url(r'^friend/favorites/$', views.friend_favorites, name="friend_favorites"),
	url(r'^friend/block_list/$', views.block_list, name="block_list"),
	#기능 부분
	url(r'^friend_add/(?P<pk>\d+)/$', views.friend_add , name='friend_add'),
	url(r'^friend/(?P<pk>\d+)/block_cancle/$', views.block_cancle, name="block_cancle"),
    url(r'^friend_accept/(?P<pk>\d+)/$', views.friend_accept, name="friend_accept"),
    url(r'^friend_reject/(?P<pk>\d+)/$', views.friend_reject, name="friend_reject"),
    url(r'^friend_cancel/(?P<pk>\d+)/$', views.friend_cancel, name="friend_cancel"),
    url(r'^friend_remove/(?P<pk>\d+)/$', views.friend_remove, name="friend_remove"),
]

#회원정보 수정
urlpatterns += [
	url(r'^setup_auth/$', views.setup_auth, name="setup_auth"),
	url(r'^preference/$', views.preference, name="preference"),
	url(r'^preference_design/$', views.preference_design, name="preference_design"),
	url(r'^preference_security/$', views.preference_security, name="preference_security"),
	url(r'^sign_out/(?P<pk>\d+)?/$', views.sign_out, name="sign_out"),
]