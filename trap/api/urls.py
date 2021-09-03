from django.conf.urls import url
from django.urls import path

from api import views
from api.views import get_swagger

schema_view = get_swagger()

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('create_comment', views.CreateCommentView.as_view({'post': 'create'})),
    path('first_level', views.FirstLevelCommentsView.as_view({'get': 'list'})),
    path('child_comments', views.ChildCommentsView.as_view({'get': 'list'}))
]
