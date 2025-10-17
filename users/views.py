
from rest_framework import viewsets, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import *
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer, RegisterSerializer
from .filters import PaymentFilter


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        #  Create product
        product_name = payment.course.title if payment.course else payment.lesson.title
        product = create_stripe_product(product_name)
        payment.stripe_product_id = product["id"]

        #  Create price
        price = create_stripe_price(product["id"], float(payment.amount))
        payment.stripe_price_id = price["id"]

        # Create checkout session
        session = create_stripe_session(
            price_id=price["id"],
            success_url="http://127.0.0.1:8000/api/users/payment/success/",
            cancel_url="http://127.0.0.1:8000/api/users/payment/cancel/",
        )
        payment.stripe_session_id = session["id"]
        payment.stripe_payment_url = session["url"]

        payment.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        payment = self.get_queryset().last()
        return Response({"payment_url": payment.stripe_payment_url}, status=status.HTTP_201_CREATED,)


class PaymentSuccessView(APIView):
    permission_classes = [AllowAny]  # JW

    def get(self, request):
        return Response({"message": "Оплата успешна!"})


class PaymentCancelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Оплата не успешна"})

# Регистрация (доступна всем)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


# CRUD для пользователей (только для авторизованных)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]