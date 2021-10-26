import django_filters

from .models import Issued_to, User_Master

class UserFilters(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='iexact')

    class meta:
        model = User_Master
        fields = "__all__"


class IssuedToFilters(django_filters.FilterSet):
    asset_id = django_filters.CharFilter(lookup_expr='iexact')
    # Users = django_filters.CharFilter()

    class meta:
        model = Issued_to
        fields = "__all__"

class IssuedToFilterss(django_filters.FilterSet):
    asset_id = django_filters.CharFilter(lookup_expr='iexact')
    
    class meta:
        model = Issued_to
        fields = "__all__"