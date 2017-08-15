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

	def __self__(self):
		return self.author.username
		
class Address(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	address = models.TextField('주소')

class Photo(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	photo = models.ImageField('사진', upload_to='newspeed/%Y/%m/%d/')

class Comment(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	message = models.TextField('댓글내용')


class Postprivacy(models.Model):
    policy = models.CharField('정책',max_length=15)

    def __str__(self):
        return self.policy