import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(fields=('date',), field_labels={'payment_date': 'Дата оплаты',})

    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],
            'lesson': ['exact'],
            'payment_method': ['exact'],
        }