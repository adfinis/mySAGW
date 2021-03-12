from faker import Faker
from faker.providers.date_time import Provider as DateTimeProvider
from faker.providers.phone_number import Provider as PhoneNumberProvider
from localized_fields.util import get_language_codes


class MultilangProvider(DateTimeProvider):
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


class SwissPhoneNumberProvider(PhoneNumberProvider):
    # https://de.wikipedia.org/wiki/Rufnummer#Schreibweisen
    _vorwahlen = (76, 77, 78, 79, 41, 44, 31, 56)
    formats = (
        *[f"+41{v}#######" for v in _vorwahlen],
        *[f"+41 {v} ### ## ##" for v in _vorwahlen],
        *[f"0{v}#######" for v in _vorwahlen],
        *[f"0{v} ### ## ##" for v in _vorwahlen],
        *[f"0041{v}#######" for v in _vorwahlen],
        *[f"0041 {v} ### ## ##" for v in _vorwahlen],
    )
