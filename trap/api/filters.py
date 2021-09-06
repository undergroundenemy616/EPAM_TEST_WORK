import django_filters
from comments.models import Comment
from django.db.models import Q
from django_filters import rest_framework


class CommentFilter(rest_framework.FilterSet):
    interval = django_filters.CharFilter(field_name='interval', method='interval_filter')
    order_by = django_filters.OrderingFilter(fields=('created_at', 'date'))
    comment = django_filters.CharFilter(field_name='id')

    class Meta:
        model = Comment
        fields = [
            'reply_to',
            'owner',
            'profile',
            'post'
        ]

    def interval_filter(self, queryset, name, value):
        intervals = value.split(',')
        return queryset.filter((Q(created_at__lte=intervals[1]) & Q(created_at__gte=intervals[0])))
