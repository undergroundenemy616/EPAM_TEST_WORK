import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CommentManager(models.Manager):
    use_in_migrations = True

    def get_entity(self, comment_type, entity_id):
        if comment_type == 'reply_to':
            comment = Comment.objects.get(reply_to__pk=entity_id)
        elif comment_type == 'post':
            comment = Comment.objects.get(post__pk=entity_id, reply_to=None)
        else:
            comment = Comment.objects.get(profile_pk=entity_id, reply_to=None)
        return comment


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

    objects = CommentManager()

    class Meta:
        verbose_name = _('комментарий')
        verbose_name_plural = _('комментарии')

    def get_all_children(self, include_self=True):
        comments = []
        if include_self:
            comments.append(self)
        for comment in Comment.objects.filter(reply_to=self):
            _r = comment.get_all_children(include_self=True)
            if 0 < len(_r):
                comments.extend(_r)
        return comments

    @classmethod
    def get_entity(cls, comment_type, entity_id):
        if comment_type == 'reply_to':
            comment = cls.__class__.objects.get(reply_to__pk=entity_id)
        elif comment_type == 'post':
            comment = cls.__class__.objects.get(post__pk=entity_id, reply_to=None)
        else:
            comment = cls.__class__.objects.get(profile_pk=entity_id, reply_to=None)
        return comment

    def __str__(self):
        return self.title

