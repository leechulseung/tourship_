from django.conf.urls import url
from group import views

urlpatterns = [
	url(r'^$', views.tourship, name="tourship"),
]