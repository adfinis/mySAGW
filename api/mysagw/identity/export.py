class IdentityExport:
    values = (
        "first_name",
        "last_name",
        "is_organisation",
        "organisation_name",
        "email",
    )

    def _fetch_related_strings(self, manager, field):
        m2m_strings = []
        for entry in manager.iterator():
            m2m_strings.append(str(getattr(entry, field)))
        return m2m_strings

    def fetch_identity_data(self, identity):
        data = {value: getattr(identity, value) for value in self.values}

        data["additional_emails"] = "\n".join(
            self._fetch_related_strings(identity.additional_emails, "email")
        )
        data["phone_numbers"] = "\n".join(
            self._fetch_related_strings(identity.phone_numbers, "phone")
        )

        return data

    def export(self, qs):
        records = []
        for identity in qs.iterator():
            records.append(self.fetch_identity_data(identity))

        return records
