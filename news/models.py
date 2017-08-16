from django.db import models
from django.conf import settings

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField('제목',max_length=120)
	content = models.TextField('내용')
	tourday = models.DateField('여행날짜')
	privacy = models.ForeignKey('Postprivacy',verbose_name='Privacy related',
        related_name='%(app_label)s_%(class)ss')
	location = models.TextField('위도/경도')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	main_photo = models.ImageField('사진', blank=True,upload_to='main_photo/%Y/%m/%d/')
	like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='Like') # post.like_set 으로 접근 가능
	def __self__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.main_photo.delete()
		for photo in self.photo_set.all():
			photo.file.delete()
			photo.delete()
		super(Post, self).delete(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Address(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	address = models.TextField('주소')

class Photo(models.Model):
    post = models.ForeignKey('Post')
    file = models.ImageField('사진', blank=True, upload_to='sub_photo/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

class Comment(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=' user related',
        related_name='%(app_label)s_%(class)ss')
	message = models.TextField('댓글내용')
	created_at = models.DateTimeField('작성일',auto_now_add=True)
	updated_at =models.DateTimeField('수정일', auto_now=True)

class Postprivacy(models.Model):
    policy = models.CharField('정책',max_length=15)

    def __str__(self):
        return self.policy