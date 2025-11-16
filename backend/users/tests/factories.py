import factory
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances in tests."""

    class Meta:
        model = User
        django_get_or_create = ('email',)

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('text', max_nb_chars=200)
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        """Set password after user creation."""
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('defaultPassword123!')
