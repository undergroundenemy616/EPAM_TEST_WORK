from comments.models import Comment, Post, Profile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


class BaseCommentSerializer(serializers.ModelSerializer):
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True)
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = '__all__'
        abstract = True


class CreateCommentSerializer(BaseCommentSerializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('reply_to') and not attrs.get('post') and not attrs.get('profile'):
            raise ValidationError('Type of comment is required ')
        comment_type_attrs = [attrs.get('reply_to'), attrs.get('post'), attrs.get('profile')]
        if len([attr for attr in comment_type_attrs if attr is not None]) > 1:
            raise ValidationError('Comment must have just one type')
        return attrs


class ChildCommentsViewSerializer(BaseCommentSerializer):
    def validate(self, attrs):
        comment_type = self.context['request'].query_params.get('type')
        entity_id = self.context['request'].query_params.get('entity_id')
        if not comment_type:
            raise ValidationError('Type of comment is required ')
        if not entity_id:
            raise ValidationError('Id if entity is required')
        if comment_type not in ['reply_to', 'post', 'profile']:
            raise ValidationError('Invalid type of comment ')
        if comment_type == 'reply_to':
            get_object_or_404(Comment, pk=entity_id)
        elif comment_type == 'post':
            get_object_or_404(Post, pk=entity_id)
        else:
            get_object_or_404(Profile, pk=entity_id)
        attrs['comment_type'] = comment_type
        attrs['entity_id'] = entity_id
        return attrs
