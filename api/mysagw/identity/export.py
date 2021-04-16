from collections import OrderedDict


class IdentityExport:
    values = (
        "first_name",
        "last_name",
        "localized_salutation",
        "is_organisation",
        "organisation_name",
        "email",
    )

    address_values = (
        "address_addition",
        "street_and_number",
        "po_box",
        "postcode",
        "town",
        "country",
    )

    def _str_or_empty(self, value):
        map = {True: 1, False: 0, None: ""}
        return map.get(value, str(value))

    def _fetch_related_strings(self, manager, field):
        m2m_strings = []
        for entry in manager.iterator():
            m2m_strings.append(self._str_or_empty(getattr(entry, field)))
        return m2m_strings

    def fetch_identity_data(self, identity):
        # pyexcel orders the keys alphabetically, if a plain dictionary is used.
        # This is still valid for python >= 3.6
        data = OrderedDict(
            {
                value: self._str_or_empty(getattr(identity, value))
                for value in self.values
            }
        )

        data["additional_emails"] = "\n".join(
            self._fetch_related_strings(identity.additional_emails, "email")
        )
        data["phone_numbers"] = "\n".join(
            self._fetch_related_strings(identity.phone_numbers, "phone")
        )

        if identity.addresses.exists():
            address = identity.addresses.get(default=True)
            data.update(
                {
                    value: self._str_or_empty(getattr(address, value))
                    for value in self.address_values
                }
            )

        return data

    def export(self, qs):
        records = []
        for identity in qs.iterator():
            records.append(self.fetch_identity_data(identity))

        return records
