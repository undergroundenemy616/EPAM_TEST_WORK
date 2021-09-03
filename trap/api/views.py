from typing import Any

from comments.models import Comment
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.pagination import DynamicPageNumberPagination
from api.serializers import (BaseCommentSerializer,
                             ChildCommentsViewSerializer,
                             CreateCommentSerializer)


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.host = '127.0.0.1:8000'
        schema.schemes = [f'http', f'https']
        return schema


def get_swagger() -> Any:
    swagger = get_schema_view(
        openapi.Info(
            title="EPAM API",
            default_version='v1',
            contact=openapi.Contact(email="ВВЕДИ СВОЮ ПОЧТУ НИКИТА"),
        ),
        public=True,
        generator_class=APISchemeGenerator
    )
    return swagger


class CreateCommentView(CreateModelMixin, GenericViewSet):
    serializer_class = CreateCommentSerializer
    queryset = Comment.objects.select_related('reply_to', 'post', 'profile')
    permission_classes = [AllowAny]


class FirstLevelCommentsView(ListModelMixin, GenericViewSet):
    serializer_class = BaseCommentSerializer
    queryset = Comment.objects.select_related('reply_to', 'post', 'profile').filter(reply_to=None)
    permission_classes = [AllowAny]
    pagination_class = DynamicPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('post', 'profile')


class ChildCommentsView(ListModelMixin, GenericViewSet):
    serializer_class = ChildCommentsViewSerializer
    queryset = Comment.objects.select_related('parent', 'post', 'profile')
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        comment_type = serializer.validated_data['comment_type']
        entity_id = serializer.validated_data['entity_id']
        comments = list(Comment.objects.get_entity(comment_type=comment_type, entity_id=entity_id).get_all_children(include_self=True))
        return Response(BaseCommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)
