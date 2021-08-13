from collections import OrderedDict


def _str_or_empty(value):
    map = {True: 1, False: 0, None: ""}
    return map.get(value, str(value))


def _fetch_related_strings(manager, field):
    m2m_strings = []
    for entry in manager.iterator():
        m2m_strings.append(_str_or_empty(getattr(entry, field)))
    return m2m_strings


class IdentityExport:
    FIELDS = {
        "first_name": lambda i, a: i.first_name,
        "last_name": lambda i, a: i.last_name,
        "localized_salutation": lambda i, a: i.localized_salutation,
        "language": lambda i, a: i.language,
        "is_organisation": lambda i, a: i.is_organisation,
        "organisation_name": lambda i, a: i.organisation_name,
        "email": lambda i, a: i.email,
        "additional_emails": lambda i, a: "\n".join(
            _fetch_related_strings(i.additional_emails, "email")
        ),
        "phone_numbers": lambda i, a: "\n".join(
            _fetch_related_strings(i.phone_numbers, "phone")
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
        for identity in qs.iterator():
            identity_data = self.fetch_identity_data(identity, fields)

            if not ignore_empty or any(identity_data.values()):
                records.append(identity_data)

        return records
