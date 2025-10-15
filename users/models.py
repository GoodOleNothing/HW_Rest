from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from materials.models import Course, Lesson
from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = PhoneNumberField(blank=True, unique=True, verbose_name='Телефон', null=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name='Страна')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь'
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, related_name='course_payments', verbose_name='Оплаченный курс'
    )

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='lesson_payments', verbose_name='Оплаченный урок'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')

    payment_method = models.CharField( max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        if self.course:
            paid_item = f"Курс: {self.course.title}"
        elif self.lesson:
            paid_item = f"Урок: {self.lesson.title}"
        else:
            paid_item = "Не указано"
        return f"{self.user.email} — {paid_item} ({self.amount} руб.)"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
