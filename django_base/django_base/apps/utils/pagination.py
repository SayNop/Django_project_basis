from rest_framework.pagination import PageNumberPagination

from .response import success_response


class MyPagination(PageNumberPagination):

    page_size_query_param = 'pagesize'
    max_page_size = 20

    # custom response format
    def get_paginated_response(self, data=None, msg='OK', cont='list'):
        return success_response(msg, {
            'total': self.page.paginator.count,
            'page': self.page.number,
            'pagesize': self.page_size,
            cont: data
        })
