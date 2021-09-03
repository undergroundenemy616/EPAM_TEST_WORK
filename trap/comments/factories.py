import factory
from django.contrib.auth.hashers import make_password
from factory import LazyAttributeSequence
from utils.fake import my_faker

from .models import Comment, Post, Profile, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: my_faker.unique.uuid4())
    email = LazyAttributeSequence(lambda o, n: f'{my_faker.unique.email()}')
    date_joined = factory.Sequence(lambda n: my_faker.date_time_between(start_date='-3d'))
    username = LazyAttributeSequence(lambda o, n: f'{my_faker.unique.user_name()}')
    password = factory.LazyFunction(lambda: make_password('pi3.1415'))


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: my_faker.unique.uuid4())
    first_name = factory.Sequence(lambda n: my_faker.first_name())
    middle_name = factory.Sequence(lambda n: my_faker.middle_name())
    last_name = factory.Sequence(lambda n: my_faker.last_name())
    phone_number = factory.Sequence(lambda n: my_faker.phone_number())
    birth_date = factory.Sequence(lambda n: my_faker.date())
    user = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: my_faker.unique.uuid4())
    title = factory.Sequence(lambda n: 'Post #{}'.format(n))
    text = factory.Sequence(lambda n: 'Text of post #{}'.format(n))
    author = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
        django_get_or_create = ('id',)

    id = factory.Sequence(lambda n: my_faker.unique.uuid4())
    title = factory.Sequence(lambda n: 'Comment #{}'.format(n))
    body = factory.Sequence(lambda n: 'Body of comment #{}'.format(n))
    reply_to = factory.SubFactory('comments.factories.CommentFactory')
    post = factory.SubFactory(PostFactory)
    profile = factory.SubFactory(ProfileFactory)







