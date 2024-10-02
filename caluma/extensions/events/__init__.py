# Import all modules in this folder so the event receivers are registered
# automatically without having to define each file as caluma event receiver
# module

from . import case, work_item, form  # noqa: F401
