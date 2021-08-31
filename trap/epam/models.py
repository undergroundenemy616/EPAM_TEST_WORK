import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Comment(models.Model):
    # essence = models.ForeignKey(on_delete=models.CASCADE, related_name='Сущность') - Связь  с нашими сущностями
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
