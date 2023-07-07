from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404

from .response import my_response


class CustomModelViewSet(ModelViewSet):

    def get_object(self):
        queryset = self.queryset.model.objects.all()
        # self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # return Response({'status': 0, 'message': '获取列表成功', 'data': serializer.data})
        return my_response(0, 'get list success', serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # return Response({'status': 0, 'message': '获取详情成功', 'data': serializer.data})
        return my_response(0, 'retrieve success', serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # let exception handler change response format

        # valid exception - change response format
        # is_valid = serializer.is_valid(raise_exception=False)
        # if not is_valid:
        #     return Response({'status': 1, 'message': serializer.errors})

        self.perform_update(serializer)
        self.perform_create(serializer)
        # return Response({'code': 0, 'message': '新增成功', 'data': serializer.data})
        return my_response(0, 'create success', serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # return Response({'status': 0, 'message': '修改成功', 'data': serializer.data})
        return my_response(0, 'update success', serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return my_response(0, 'delete success', None)
