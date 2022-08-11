# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_db_migrations_not_applied[admin] 1"] = {
    "caches": [{"default": {"ok": True}}],
    "database migrations": [{"default": {"ok": False}}],
    "database models": [{"default": {"ok": True}}],
    "databases": [{"default": {"ok": True}}],
}

snapshots["test_healthz_permissions[admin-200] 1"] = {
    "caches": [{"default": {"ok": True}}],
    "database migrations": [{"default": {"ok": True}}],
    "database models": [{"default": {"ok": True}}],
    "databases": [{"default": {"ok": True}}],
}

snapshots["test_healthz_permissions[staff-200] 1"] = {
    "caches": [{"default": {"ok": True}}],
    "database migrations": [{"default": {"ok": True}}],
    "database models": [{"default": {"ok": True}}],
    "databases": [{"default": {"ok": True}}],
}
