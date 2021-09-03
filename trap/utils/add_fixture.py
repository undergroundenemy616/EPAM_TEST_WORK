from comments.factories import PostFactory, CommentFactory, ProfileFactory, UserFactory
from comments.models import Post, Comment, Profile, User


# def add_profiles(self):
#     self.stdout.write(self.style.WARNING(f'Starting create profiles, wait for a moment...'))
#     try:
#         for i in range(1000):
#             ProfileFactory()
#             if i % 100 == 0:
#                 self.stdout.write(self.style.SUCCESS(f'{i}/1000 profiles created...'))
#         self.stdout.write(self.style.SUCCESS(f'Profiles created successfully'))
#     except Exception as exc:
#         self.stdout.write(self.style.ERROR(f'Failed to create profiles, error: {exc}'))