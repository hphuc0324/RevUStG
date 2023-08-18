from .models import *
import django_filters
from django_filters import RangeFilter, ChoiceFilter


class ProductFilter(django_filters.FilterSet):
    min_price = RangeFilter(field_name='sell_price', label="Min price")
    class Meta:
        model = Product
        fields = ['min_price', 'platForm']





        