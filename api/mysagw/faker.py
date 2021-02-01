from faker import Faker
from faker.providers.date_time import Provider
from localized_fields.util import get_language_codes


class MultilangProvider(Provider):
    """
    Create dictionary compatible with `LocalizedField`.

    A value with given `faker_provider` is created for given languages.
    """

    def multilang(self, faker_provider, languages=None, **kwargs):
        languages = languages if languages is not None else get_language_codes()
        value = {}
        for language in languages:
            value[language] = getattr(Faker(language), faker_provider)(*kwargs)

        return value
