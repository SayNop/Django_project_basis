from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):

    page_size_query_param = 'pagesize'
    max_page_size = 20

    # custom response format
    def get_paginated_response(self, data=None, msg='OK', cont='list'):
        return Response({
            "code": 0,
            "success": True,
            "message": msg,
            "data": {
                'total': self.page.paginator.count,
                'totalPages': self.page.paginator.num_pages,
                'page': self.page.number,
                'pagesize': self.page_size,
                cont: data
            }
        })
