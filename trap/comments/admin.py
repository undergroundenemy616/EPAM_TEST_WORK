from django.contrib import admin

from comments.models import Comment, Post, Profile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'password', 'email', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'phone', 'birth_date', 'user')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'reply_to', 'post', 'profile')

