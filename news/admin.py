from django.contrib import admin
from .models import Post, Comment, Address, Photo, Postprivacy, Block_user, Report_Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	pass

@admin.register(Postprivacy)
class PostprivacyAdmin(admin.ModelAdmin):
	pass


@admin.register(Block_user)
class Block_userAdmin(admin.ModelAdmin):
	pass

@admin.register(Report_Post)
class Report_PostAdmin(admin.ModelAdmin):
	pass