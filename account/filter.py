import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

import django_filters
from django import forms

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'class': 'my-custom-date-filter'}),
    )
    end_date = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'class': 'my-custom-date-filter'}),
    )
    note = django_filters.CharFilter(
        field_name='note',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'my-custom-char-filter'}),
    )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']

