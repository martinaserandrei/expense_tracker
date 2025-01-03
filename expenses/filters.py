import django_filters
from expenses.models import Transaction, Category
from django import forms

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name='type',  # Refers to Transaction.type
        lookup_expr='iexact',  # Case-insensitive exact match
        label='Transaction Type',
        empty_label='Any',  # Optional label
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),  # Refers to Category model instances
        field_name='category',  # Refers to the ForeignKey in Transaction
        label='Category',
        empty_label='All',  # Optional label
    )
    min_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte',  # Greater than or equal to
        label='Minimum Amount',
    )
    max_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte',  # Less than or equal to
        label='Maximum Amount',
    )
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'min_amount', 'max_amount', 'start_date', 'end_date']
