from caluma.caluma_form import models, schema
from caluma.extensions.visibilities import MySAGWVisibility


def test_visibilities_default(
    db, form, admin_info,
):
    vis = MySAGWVisibility()

    queryset = models.Form.objects.all()

    filtered = vis.filter_queryset(schema.Form, queryset, admin_info)

    assert filtered.count() == 1
