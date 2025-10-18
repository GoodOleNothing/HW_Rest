from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Проверяет всех пользователей, и если last_login > 30 дней,
    делает их неактивными.
    """
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=month_ago)

    count = inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"
