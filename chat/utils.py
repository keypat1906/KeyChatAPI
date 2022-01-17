
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import InvalidPage
from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.response import Response
from collections import OrderedDict
import json

class EventCustomPagination(PageNumberPagination):

    page_size_default = 100
    def __init__(self, request):
        self.max_page_size = 100
        self.page_size_query_param = 'page_size'
        try:

            # Trying to read page_size from query parameters
            self.page_size = request.query_params.get('page_size')

            # Get the max page size preference
            max_page_size_configured = 100

            if self.page_size is None and max_page_size_configured is None:
                # Parameter is not defined in query params and there's no configuration value
                self.page_size = self.page_size_default

            elif (self.page_size is None and max_page_size_configured) or \
                    (self.page_size and int(self.page_size) > max_page_size_configured):
                # Parameter is not defined in query params, we must take it from configuration or
                # Page size greater than configured value, we assign the configured value
                self.page_size = max_page_size_configured

        except ObjectDoesNotExist:
            self.page_size = self.page_size_default

    def paginate_queryset(self, queryset, request, view=None):
        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)
        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):

        return Response(OrderedDict([('max_display_count', 100),  ('total_count', self.page.paginator.count),('results', data)]))

