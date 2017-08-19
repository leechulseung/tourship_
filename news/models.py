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
	main_photo = models.ImageField('사진',upload_to='main_photo/%Y/%m/%d/')
	like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,
                                           related_name='like_user_set',
                                           through='Like') # post.like_set 으로 접근 가능

	def __str__(self):
		return self.title

	def delete(self, *args, **kwargs):
		self.main_photo.delete()
		for photo in self.photo_set.all():
			photo.file.delete()
			photo.delete()
		super(Post, self).delete(*args, **kwargs)

	@property
	def like_count(self):
		return self.like_user_set.count()

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
    file = models.ImageField('서브사진', blank=True, upload_to='sub_photo/%Y/%m/%d/')
    uploaded_at =  models.DateTimeField(auto_now_add=True)

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


class Block_user(models.Model):
    block_man = models.CharField('차단된 유저명',max_length=20)  #차단당한 유저이름
    block_man_id = models.CharField('차단된 유저ID',max_length=20)  #차단당한 유저ID
    reasons = models.CharField('차단사유',max_length=20)  #차단사유
    author = models.ForeignKey(settings.AUTH_USER_MODEL) #차단한 유저

    def __str__(self):
        return self.author.username

class Report_Post(models.Model):
    user = models.CharField('유저명',max_length=20)
    title = models.ForeignKey('Post',default = 1)
    content = models.CharField('신고내용',max_length=100)

    def __str__(self):
        return self.content

class Bookingpost(models.Model):
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)ss_from')
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True, related_name='%(app_label)s_%(class)ss_to')
	title = models.CharField('제목',max_length=120)
	content = models.TextField('내용')
	address = models.TextField('주소')
	location = models.TextField('위도/경도')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title	        