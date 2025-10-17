from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5                    # количество объектов на одной странице по умолчанию
    page_size_query_param = 'page_size'  # параметр, который можно передавать в URL для изменения page_size
    max_page_size = 20               # максимальное количество объектов на странице