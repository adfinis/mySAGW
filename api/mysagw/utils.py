def build_url(*fragments, **options):
    sep = "/"
    url = sep.join([fragment.strip(sep) for fragment in fragments])

    if options.get("trailing", False):
        url += sep

    return url
