from caluma.caluma_core.types import Node
from caluma.caluma_core.visibilities import BaseVisibility, filter_queryset_for


class MySAGWVisibility(BaseVisibility):
    @filter_queryset_for(Node)
    def filter_queryset_for_all(self, node, queryset, info):
        return queryset
