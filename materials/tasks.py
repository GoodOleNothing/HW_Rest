from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """
    Асинхронная задача для рассылки писем подписчикам курса.
    """
    course = Course.objects.get(id=course_id)

    # проверяем, не обновлялся ли курс за последние 4 часа
    if course.updated_at and timezone.now() - course.updated_at < timedelta(hours=4):
        print(f"Курс '{course.title}' обновлялся недавно — рассылка отменена.")
        return

    # получаем всех подписанных пользователей
    subscriptions = Subscription.objects.filter(course=course)
    subscribers = [s.user.email for s in subscriptions if s.user.email]

    if not subscribers:
        print(f"Нет подписчиков для курса '{course.title}'")
        return

    subject = f"Обновление курса: {course.title}"
    message = f"Материалы курса '{course.title}' были обновлены. Зайдите, чтобы посмотреть изменения."
    from_email = "noreply@mysite.com"

    # Отправляем письма всем подписчикам
    send_mail(subject, message, from_email, subscribers)

    # обновляем время последнего обновления
    course.updated_at = timezone.now()
    course.save()

    print(f"Рассылка для курса '{course.title}' завершена. Отправлено писем: {len(subscribers)}")
