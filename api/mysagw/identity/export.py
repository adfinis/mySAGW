from collections import OrderedDict


def _str_or_empty(value):
    mapping = {True: 1, False: 0, None: ""}
    return mapping.get(value, str(value))


def _fetch_related_strings(manager, field):
    return [_str_or_empty(getattr(entry, field)) for entry in manager.iterator()]


class IdentityExport:
    FIELDS = {
        "first_name": lambda i, a: i.first_name,
        "last_name": lambda i, a: i.last_name,
        "localized_salutation": lambda i, a: i.localized_salutation,
        "localized_title": lambda i, a: i.localized_title,
        "language": lambda i, a: i.language,
        "is_organisation": lambda i, a: i.is_organisation,
        "organisation_name": lambda i, a: i.organisation_name,
        "email": lambda i, a: i.email,
        "additional_emails": lambda i, a: "\n".join(
            _fetch_related_strings(i.additional_emails, "email"),
        ),
        "phone_numbers": lambda i, a: "\n".join(
            _fetch_related_strings(i.phone_numbers, "phone"),
        ),
        "address_addition_1": lambda i, a: "" if not a else a.address_addition_1,
        "address_addition_2": lambda i, a: "" if not a else a.address_addition_2,
        "address_addition_3": lambda i, a: "" if not a else a.address_addition_3,
        "street_and_number": lambda i, a: "" if not a else a.street_and_number,
        "po_box": lambda i, a: "" if not a else a.po_box,
        "postcode": lambda i, a: "" if not a else a.postcode,
        "town": lambda i, a: "" if not a else a.town,
        "country": lambda i, a: "" if not a else a.country.name,
    }

    def fetch_identity_data(self, identity, fields):
        address = None
        if identity.addresses.exists():
            address = identity.addresses.get(default=True)

        data = OrderedDict()

        for field_key, field_getter in fields.items():
            data[field_key] = _str_or_empty(field_getter(identity, address))

        return data

    def export(self, qs, include_fields=None, ignore_empty=False):
        include_fields = include_fields if include_fields else self.FIELDS.keys()
        fields = {name: self.FIELDS[name] for name in include_fields}

        records = []
        for identity in qs.iterator(2000):
            identity_data = self.fetch_identity_data(identity, fields)

            if not ignore_empty or any(identity_data.values()):
                records.append(identity_data)

        return records


class MembershipExport:
    FIELDS = {
        "first_name": lambda m, a: m.identity.first_name,
        "last_name": lambda m, a: m.identity.last_name,
        "localized_salutation": lambda m, a: m.identity.localized_salutation,
        "localized_title": lambda m, a: m.identity.localized_title,
        "language": lambda m, a: m.identity.language,
        "email": lambda m, a: m.identity.email,
        "address_addition_1": lambda m, a: "" if not a else a.address_addition_1,
        "address_addition_2": lambda m, a: "" if not a else a.address_addition_2,
        "address_addition_3": lambda m, a: "" if not a else a.address_addition_3,
        "street_and_number": lambda m, a: "" if not a else a.street_and_number,
        "po_box": lambda m, a: "" if not a else a.po_box,
        "postcode": lambda m, a: "" if not a else a.postcode,
        "town": lambda m, a: "" if not a else a.town,
        "country": lambda m, a: "" if not a else a.country.name,
        "organisation": lambda m, a: m.organisation.organisation_name,
        "role": lambda m, a: "" if not m.role else m.role.title[m.identity.language],
        "inactive": lambda m, a: m.inactive,
        "tenure": lambda m, a: ""
        if not m.time_slot
        else f"{m.time_slot.lower if m.time_slot.lower else ''} - {m.time_slot.upper if m.time_slot.upper else ''}",
        "next_election": lambda m, a: m.next_election,
    }

    def fetch_membership_data(self, membership, fields):
        address = None
        if membership.identity.addresses.exists():
            address = membership.identity.addresses.get(default=True)

        data = OrderedDict()

        for field_key, field_getter in fields.items():
            data[field_key] = _str_or_empty(field_getter(membership, address))

        return data

    def export(self, qs, include_fields=None, ignore_empty=False):
        include_fields = include_fields if include_fields else self.FIELDS.keys()
        fields = {name: self.FIELDS[name] for name in include_fields}

        records = []
        for membership in qs.iterator(2000):
            membership_data = self.fetch_membership_data(membership, fields)

            if not ignore_empty or any(membership_data.values()):
                records.append(membership_data)

        return records
