from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from ..identity.models import Identity
from . import email_texts, models


class CaseAccessSerializer(serializers.ModelSerializer):
    included_serializers = {
        "identity": "mysagw.identity.serializers.PublicIdentitySerializer",
    }

    class Meta:
        model = models.CaseAccess
        fields = (
            "case_id",
            "identity",
            "email",
        )
        extra_kwargs = {
            "identity": {"required": False, "read_only": True},
        }

    def validate(self, *args, **kwargs):
        validated_data = super().validate(*args, **kwargs)

        try:
            validated_data["identity"] = Identity.objects.get(
                email__iexact=validated_data["email"]
            )
            validated_data.pop("email")
        except Identity.DoesNotExist:
            pass

        if models.CaseAccess.objects.filter(
            email__iexact=validated_data.get("email"),
            case_id=validated_data["case_id"],
            identity=validated_data.get("identity"),
        ).exists():
            raise ValidationError("Case already exists!")

        return validated_data

    def create(self, validated_data):
        instance = super().create(validated_data)

        subject = email_texts.EMAIL_SUBJECT_INVITE_REGISTER
        body = email_texts.EMAIL_BODY_INVITE_REGISTER.format(link=settings.SELF_URI)
        email = instance.email

        if instance.identity:
            subject = email_texts.EMAIL_INVITE_SUBJECTS[instance.identity.language]
            body = email_texts.EMAIL_INVITE_BODIES[instance.identity.language].format(
                first_name=instance.identity.first_name or "",
                last_name=instance.identity.last_name or "",
                link=f"{settings.SELF_URI}/cases/{instance.case_id}",
            )
            email = instance.identity.email

        send_mail(
            subject,
            body,
            settings.MAILING_SENDER,
            [email],
            fail_silently=True,
        )

        return instance
