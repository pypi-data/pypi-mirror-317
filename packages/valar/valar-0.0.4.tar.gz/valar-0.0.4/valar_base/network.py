from django.http import JsonResponse


class ValaResponse(JsonResponse):
    def __init__(self, data, message='', _type='info'):
        data = {
            'result': data,
            'message': message,
            'type': _type
        }
        super(ValaResponse, self).__init__(data, safe=False)
