from django.db import models

class Post(models.Model):
	title = models.CharField('제목',max_length=120)
	content = models.TextField('내용')
	tourday = models.DateField('여행날짜')
	privacy = models.ForeignKey('Postprivacy',verbose_name='Privacy related',
        related_name='%(app_label)s_%(class)ss')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	main_photo = models.ImageField('사진', blank=True,upload_to='main_photo/%Y/%m/%d/')
	def __str__(self):
		return self.title

class Address(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	address = models.TextField('주소')

class Photo(models.Model):
    pos = models.ForeignKey('Post')
    file = models.ImageField('사진', blank=True, upload_to='sub_photo/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pos.title

class Comment(models.Model):
	post = models.ForeignKey('Post', verbose_name='post related',
		related_name='%(app_label)s_%(class)ss')
	message = models.TextField('댓글내용')

class Postprivacy(models.Model):
    policy = models.CharField('정책',max_length=15)

    def __str__(self):
        return self.policy