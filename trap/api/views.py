from typing import Any

from comments.models import Comment
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import CommentFilter
from api.pagination import DynamicPageNumberPagination
from api.serializers import (BaseCommentSerializer, ChildCommentsSerializer,
                             CreateCommentSerializer)


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.host = '0.0.0.0:80'
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


class CommentsViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = BaseCommentSerializer
    queryset = Comment.objects.select_related('reply_to', 'post', 'profile', 'owner')
    permission_classes = [AllowAny]
    filterset_class = CommentFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = DynamicPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'get_child_comments':
            return ChildCommentsSerializer
        elif self.action == 'create':
            return CreateCommentSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=False)
    def get_child_comments(self, request, *args, **kwargs):
        first_level_comments = CommentFilter(data=request.query_params, queryset=self.get_queryset()).qs
        return Response(data=self.get_serializer(first_level_comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def download_comments_csv(self, request, *args, **kwargs):
        comments = CommentFilter(data=request.query_params, queryset=self.get_queryset()).qs
        response = Comment.queryset_to_csv_response(comments)
        return response
