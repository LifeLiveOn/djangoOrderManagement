import django_filters
from django import forms
from .models import Order


class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr='gte',
        label='start Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'my-custom-date-filter'}),
    )
    end_date = django_filters.DateFilter(
        field_name="date_created",
        lookup_expr='lte',
        label='end Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'my-custom-date-filter'}),
    )
    note = django_filters.CharFilter(
        field_name='note',
        lookup_expr='icontains',
        label='Notes:',
        widget=forms.TextInput(attrs={'class': 'my-custom-char-filter'}),
    )
    order_by = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('date_created', 'date_created')
        ),
        # labels do not need to retain order
        field_labels={
            'date_created': 'Date',
        }
    )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
