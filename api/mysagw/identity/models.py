from django.conf import settings
from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language
from django_countries.fields import CountryField
from localized_fields.fields import LocalizedCharField, LocalizedTextField
from phonenumber_field.modelfields import PhoneNumberField

from mysagw.models import HistoricalModel, TrackingModel, UniqueBooleanField, UUIDModel


class InterestCategory(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = models.CharField(max_length=255, blank=True, null=True)
    archived = models.BooleanField(default=False)
    public = models.BooleanField(default=False)


class Interest(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        InterestCategory,
        related_name="interests",
        on_delete=models.PROTECT,
    )
    archived = models.BooleanField(default=False)


class MembershipRole(UUIDModel, HistoricalModel):
    title = LocalizedCharField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    archived = models.BooleanField(default=False)
    sort = models.PositiveIntegerField(editable=False, db_index=True, default=0)

    class Meta:
        ordering = ["-sort", "title"]


class Membership(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        "Identity",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organisation = models.ForeignKey(
        "Identity",
        on_delete=models.CASCADE,
        related_name="members",
    )
    role = models.ForeignKey(
        MembershipRole,
        related_name="memberships",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    authorized = models.BooleanField(default=False)
    time_slot = DateRangeField(null=True, blank=True)
    next_election = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    inactive = models.BooleanField(default=False)


class Identity(UUIDModel, HistoricalModel, TrackingModel):
    SALUTATION_MR = "male"
    SALUTATION_MRS = "female"
    SALUTATION_NEUTRAL = "neutral"

    SALUTATION_LOCALIZED_MAP = {
        SALUTATION_MR: {"de": "Herr", "en": "Mr.", "fr": "Monsieur"},
        SALUTATION_MRS: {"de": "Frau", "en": "Mrs.", "fr": "Madame"},
        SALUTATION_NEUTRAL: {"de": "", "en": "", "fr": ""},
    }

    GREETING_LOCALIZED_MAP = {
        SALUTATION_MR: {"de": "Sehr geehrter", "en": "Dear", "fr": ""},
        SALUTATION_MRS: {"de": "Sehr geehrte", "en": "Dear", "fr": ""},
        SALUTATION_NEUTRAL: {"de": "Sehr geehrte·r", "en": "Dear", "fr": ""},
    }

    SALUTATION_CHOICES = (
        (SALUTATION_MR, SALUTATION_MR),
        (SALUTATION_MRS, SALUTATION_MRS),
        (SALUTATION_NEUTRAL, SALUTATION_NEUTRAL),
    )

    TITLE_DR = "dr"
    TITLE_PROF = "prof"
    TITLE_PROF_DR = "prof-dr"
    TITLE_PROF_EM_DR = "prof-em-dr"
    TITLE_PD_DR = "pd-dr"
    TITLE_NONE = "none"

    TITLE_LOCALIZED_MAP = {
        TITLE_DR: {"de": "Dr.", "en": "Dr.", "fr": "Dr"},
        TITLE_PROF: {"de": "Prof.", "en": "Prof.", "fr": "Prof."},
        TITLE_PROF_DR: {"de": "Prof. Dr.", "en": "Prof. Dr.", "fr": "Prof. Dr"},
        TITLE_PROF_EM_DR: {
            "de": "Prof. em. Dr.",
            "en": "Prof. em. Dr.",
            "fr": "Prof. em. Dr",
        },
        TITLE_PD_DR: {"de": "PD Dr.", "en": "PD Dr.", "fr": "PD Dr"},
        TITLE_NONE: {"de": "", "en": "", "fr": ""},
    }

    TITLE_CHOICES = (
        (TITLE_DR, TITLE_DR),
        (TITLE_PROF, TITLE_PROF),
        (TITLE_PROF_DR, TITLE_PROF_DR),
        (TITLE_PROF_EM_DR, TITLE_PROF_EM_DR),
        (TITLE_PD_DR, TITLE_PD_DR),
        (TITLE_NONE, TITLE_NONE),
    )

    idp_id = models.CharField(max_length=255, unique=True, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    organisation_slug = models.SlugField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    salutation = models.CharField(
        choices=SALUTATION_CHOICES,
        default=SALUTATION_NEUTRAL,
        max_length=7,
    )
    title = models.CharField(choices=TITLE_CHOICES, default=TITLE_NONE, max_length=14)
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    interests = models.ManyToManyField(Interest, related_name="identities", blank=True)
    is_organisation = models.BooleanField(default=False)
    is_expert_association = models.BooleanField(default=False)
    is_advisory_board = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def _get_memberships(self, only_authorized=False):
        memberships = self.memberships.filter(
            Q(inactive=False),
            Q(time_slot__isnull=True) | Q(time_slot__contains=timezone.now()),
        )
        if only_authorized:
            memberships = memberships.filter(authorized=True)
        return self.__class__.objects.filter(
            pk__in=memberships.values_list("organisation", flat=True).distinct(),
        )

    @property
    def full_name(self):
        language = get_language()
        salutation = self.SALUTATION_LOCALIZED_MAP.get(self.salutation, {}).get(
            language,
        )
        title = self.TITLE_LOCALIZED_MAP[self.title][language]
        full_name = ""
        if salutation:
            full_name = f"{salutation}"

        if title and full_name:
            full_name = f"{full_name} {title}"
        elif title:
            full_name = title

        if self.first_name and full_name:
            full_name = f"{full_name} {self.first_name}"
        elif self.first_name:
            full_name = self.first_name

        if self.last_name and full_name:
            full_name = f"{full_name} {self.last_name}"
        elif self.last_name:
            full_name = self.last_name

        return full_name

    @property
    def address_block(self):
        address_block = self.full_name
        try:
            address = self.addresses.get(default=True)
        except Address.DoesNotExist:
            return address_block

        for add in [
            address.address_addition_1,
            address.address_addition_2,
            address.address_addition_3,
        ]:
            if add:
                address_block = f"{address_block}\n{add}"

        address_block = f"{address_block}\n{address.street_and_number}"

        if address.po_box:
            address_block = f"{address_block}\n{address.po_box}"

        return f"{address_block}\n{address.postcode} {address.town}\n{address.country.name}"

    def greeting_salutation_and_name(self):
        language = get_language()
        greeting = self.GREETING_LOCALIZED_MAP[self.salutation][language]
        result = self.full_name

        if greeting:
            result = f"{greeting} {self.full_name}"

        return result

    @property
    def authorized_for(self):
        return self._get_memberships(only_authorized=True)

    @property
    def member_of(self):
        return self._get_memberships(only_authorized=False)

    @property
    def localized_salutation(self):
        return self.SALUTATION_LOCALIZED_MAP[self.salutation][self.language]

    @property
    def localized_title(self):
        return self.TITLE_LOCALIZED_MAP[self.title][self.language]

    class Meta:
        ordering = ("last_name", "first_name", "email")


class Email(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        Identity,
        related_name="additional_emails",
        on_delete=models.CASCADE,
    )
    email = models.EmailField()
    description = LocalizedCharField(blank=True, null=True, required=False)

    class Meta:
        unique_together = [["identity", "email"]]
        ordering = ("email",)


class PhoneNumber(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        Identity,
        related_name="phone_numbers",
        on_delete=models.CASCADE,
    )
    phone = PhoneNumberField()
    description = LocalizedCharField(blank=True, null=True, required=False)
    default = UniqueBooleanField(default=False, together=["identity"])

    class Meta:
        unique_together = [["identity", "phone"]]
        ordering = ("-default", "phone")


class Address(UUIDModel, HistoricalModel):
    identity = models.ForeignKey(
        Identity,
        related_name="addresses",
        on_delete=models.CASCADE,
    )
    address_addition_1 = models.CharField(max_length=255, null=True, blank=True)
    address_addition_2 = models.CharField(max_length=255, null=True, blank=True)
    address_addition_3 = models.CharField(max_length=255, null=True, blank=True)
    street_and_number = models.CharField(max_length=255)
    po_box = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = CountryField(default="CH")
    description = LocalizedCharField(blank=True, null=True, required=False)
    default = UniqueBooleanField(default=False, together=["identity"])

    class Meta:
        ordering = ("-default",)
