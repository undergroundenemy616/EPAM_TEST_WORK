import django_filters
from comments.models import Comment
from django.db.models import Q
from django_filters import rest_framework


class CommentFilter(rest_framework.FilterSet):
    """ Фильтр для сущности Comment

    Query параметры:
        interval - интервал времени для выгрузки комментариев (interval=<datetime>,<datetime>)
        order_by - поле для сортировки комментариев по дате создания (order_by=date)
        reply_to - поле для фильтрации комментариев по родительскому коммендарию (reply_to=<UUID>)
        owner - поле для фильтрации комментариев по пользователю (owner=<UUID>)
        post - поле для фильтрации комментариев по посту (post=<UUID>)
        profile - поле для фильтрации комментариев по профилю (profile=<UUID>)

    """
    interval = django_filters.CharFilter(field_name='interval', method='interval_filter')
    order_by = django_filters.OrderingFilter(fields=('created_at', 'date'))

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
