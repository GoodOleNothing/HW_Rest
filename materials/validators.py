from rest_framework import serializers
from urllib.parse import urlparse


def validate_youtube_url(value):
    """
    Проверяет, что ссылка ведет только на youtube.com
    """
    if not value:
        return value  # пустые значения допустимы

    if not value.startswith(('http://', 'https://')):
        value = 'https://' + value

    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    # Разрешаем только youtube.com
    allowed_domains = ['www.youtube.com', 'youtube.com']

    if domain not in allowed_domains:
        raise serializers.ValidationError(
            "Можно прикреплять только ссылки на YouTube."
        )

    return value
