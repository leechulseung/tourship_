from django.conf.urls import url
from news import views

urlpatterns = [
	url(r'^$', views.news_list, name="news_list"),
	url(r'^modal/$', views.modal, name="modal"),
]
