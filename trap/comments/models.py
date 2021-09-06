import csv
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    first_name = models.CharField(_('имя'), max_length=64, blank=True)
    middle_name = models.CharField(_('отчество'), max_length=64, blank=True)
    last_name = models.CharField(_('фамилия'), max_length=64, blank=True)
    phone = models.CharField(_('телефон'), max_length=64, blank=True)
    birth_date = models.DateField(_('дата рождения'), null=True, blank=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'
        ordering = ['last_name']
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Post(BaseModel):
    title = models.CharField(_('название'), max_length=128, null=False, blank=False)
    text = models.TextField(_('текст'), null=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_posts")

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')

    def __str__(self):
        return self.title


class Comment(BaseModel):
    title = models.CharField(_('название'), max_length=128, null=False, blank=True)
    body = models.TextField(_('тело'), null=False, blank=True)
    reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, default=None, blank=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('комментарий')
        verbose_name_plural = _('комментарии')

    def get_all_children(self, include_self=True) -> list:
        comments = []
        if include_self:
            comments.append(self)
        for comment in Comment.objects.filter(reply_to=self):
            _r = comment.get_all_children(include_self=True)
            if 0 < len(_r):
                comments.extend(_r)
        return comments

    @classmethod
    def queryset_to_csv_response(cls, queryset) -> HttpResponse:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="comments.csv"'
        writter = csv.writer(response)
        writter.writerow(['id', 'created_at', 'updated_at', 'title',
                          'body', 'reply_to', 'post', 'profile', 'owner'])
        for comment in queryset:
            writter.writerow([comment.id, comment.created_at, comment.updated_at, comment.title,
                              comment.body, comment.reply_to, comment.post, comment.profile, comment.owner])
        return response

    def __str__(self):
        return self.title

