from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers as drf_serializers
from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from ..identity.models import Identity
from . import models
from .email_texts import case_transfer, invite


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
                email__iexact=validated_data["email"],
            )
            validated_data.pop("email")
        except Identity.DoesNotExist:
            pass

        if models.CaseAccess.objects.filter(
            email__iexact=validated_data.get("email"),
            case_id=validated_data["case_id"],
            identity=validated_data.get("identity"),
        ).exists():
            msg = "Case already exists!"
            raise ValidationError(msg)

        return validated_data

    def create(self, validated_data):
        instance = super().create(validated_data)

        if models.CaseAccess.objects.filter(case_id=instance.case_id).count() == 1:
            return instance

        subject = invite.EMAIL_SUBJECT_INVITE_REGISTER
        body = invite.EMAIL_BODY_INVITE_REGISTER.format(link=settings.SELF_URI)
        email = instance.email

        if instance.identity:
            subject = invite.EMAIL_INVITE_SUBJECTS[instance.identity.language]
            body = invite.EMAIL_INVITE_BODIES[instance.identity.language].format(
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


class CaseTransferSerializer(drf_serializers.Serializer):
    to_remove_assignees = drf_serializers.ListField(
        child=drf_serializers.PrimaryKeyRelatedField(
            queryset=Identity.objects.filter(is_organisation=False)
        )
    )
    new_assignees = drf_serializers.ListField(
        child=drf_serializers.PrimaryKeyRelatedField(
            queryset=Identity.objects.filter(is_organisation=False)
        ),
        allow_empty=False,
    )
    case_ids = drf_serializers.ListField(
        child=drf_serializers.UUIDField(), allow_empty=False
    )

    dossier_nrs = drf_serializers.ListField(
        child=drf_serializers.CharField(), allow_empty=False
    )

    def validate(self, attrs):
        if len(attrs["dossier_nrs"]) != len(attrs["case_ids"]):
            msg = '"case_ids" and "dossier_nrs" must be of equal length.'
            raise ValidationError(msg)
        attrs["dossier_nrs_mapping"] = dict(
            zip(attrs["dossier_nrs"], attrs["case_ids"])
        )
        return super().validate(attrs)

    def create(self, validated_data):
        new_accesses = []
        for new_assignee in validated_data["new_assignees"]:
            new_accesses_for_user = []
            for dossier_nr, case_id in validated_data["dossier_nrs_mapping"].items():
                access, created = models.CaseAccess.objects.get_or_create(
                    case_id=case_id, identity=new_assignee
                )
                if created:
                    new_accesses_for_user.append((access, dossier_nr))
            if new_accesses_for_user:
                self._send_mail(new_accesses_for_user)
            new_accesses += new_accesses_for_user

        if validated_data["to_remove_assignees"]:
            to_remove = models.CaseAccess.objects.filter(
                case_id__in=validated_data["case_ids"],
                identity__in=validated_data["to_remove_assignees"],
            )
            to_remove.delete()
        return new_accesses

    def _send_mail(self, new_accesses_for_user):
        identity = new_accesses_for_user[0][0].identity
        subject = case_transfer.EMAIL_BULK_INVITE_SUBJECTS[identity.language]
        links = "\n".join(
            [
                f"{access[1]} - {settings.SELF_URI}/cases/{access[0].case_id}"
                for access in new_accesses_for_user
            ]
        )
        body = case_transfer.EMAIL_BULK_INVITE_BODIES[identity.language].format(
            first_name=identity.first_name or "",
            last_name=identity.last_name or "",
            links=links,
        )

        send_mail(
            subject,
            body,
            settings.MAILING_SENDER,
            [identity.email],
            fail_silently=True,
        )
