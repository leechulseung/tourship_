from django.db import models
from django.conf import settings


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	address = models.CharField('상세주소', max_length=50)
	birthdate = models.CharField('생일', max_length=120, blank=True)
	gender = models.CharField('성별', max_length=5)
	phone_num = models.CharField('전화번호', max_length=15)
	photo = models.ImageField('프로필사진', blank=True, upload_to='newspeed/%Y/%m/%d/')
	is_tour = models.BooleanField('여행여부', default=False)

	def __str__(self):
		return self.user.username