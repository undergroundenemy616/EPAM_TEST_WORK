from comments.models import Comment, Post, Profile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BaseCommentSerializer(serializers.ModelSerializer):
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=False)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=False)
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False, allow_null=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['owner']
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


class ChildCommentsSerializer(BaseCommentSerializer):
    def to_representation(self, instance):
        representation = super(ChildCommentsSerializer, self).to_representation(instance)
        child_comments = ChildCommentsSerializer(instance.get_all_children(include_self=False), many=True).data
        representation['child_comments'] = child_comments
        return representation
