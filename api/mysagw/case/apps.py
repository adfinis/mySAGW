from importlib import import_module

from django.apps import AppConfig


class CaseConfig(AppConfig):
    name = "mysagw.case"

    def ready(self):
        import_module("mysagw.case.signals")
