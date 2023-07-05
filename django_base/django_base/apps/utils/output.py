from rest_framework.renderers import JSONRenderer

from .response_code import SUCCESS, FRAMEWORK


# All response (include exception) will pass into this renderer
class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # goto default return: situation 1 : unknown response position   situation 2 : format complete
        if renderer_context and not(isinstance(data, dict) and 'code' in data and 'success' in data and 'message' in data):
            # dict need format
            if isinstance(data, dict) and 'message' in data:
                cache = data.copy()
                data = {
                    'code': cache.get('code', SUCCESS if renderer_context["response"].status_code == 200 else FRAMEWORK),
                    'message': cache.get('message', 'OK')
                }

            elif isinstance(data, str):
                # response is str，data or message
                cache = data
                data = {
                    'code': SUCCESS if renderer_context["response"].status_code == 200 else FRAMEWORK,
                    'message': cache,
                    'data': cache
                }

            elif renderer_context['request']._request.method == 'DELETE' and renderer_context['response'].status_code == 204:
                renderer_context['response'].status_code = 200
                data = {
                    'code': SUCCESS,
                    'message': 'Delete success'
                }

            else:
                ret = {'code': SUCCESS, 'message': 'OK', 'data': data}
                data = ret

            data['success'] = True if data['code'] == SUCCESS else False

        return super().render(data, accepted_media_type, renderer_context)
