def build_url(*fragments, **options):
    sep = "/"
    url = sep.join([fragment.strip(sep) for fragment in fragments])

    if options.get("trailing", False):
        url += sep

    return url


def format_currency(value, currency):
    if currency and (isinstance(value, (float, int))):
        value = f"{currency.upper()} {value:_.2f}".replace(".00", ".-").replace(
            "_",
            "'",
        )
    return value
