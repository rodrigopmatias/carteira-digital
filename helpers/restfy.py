import json

from django.http.response import HttpResponse, HttpResponseNotAllowed, JsonResponse
from helpers.serializer import BaseSerializer


def not_implemented_method(request):
    return HttpResponse(
        status=501,
        content_type='application/json',
        content=json.dumps({
            'message': f'Not implemented method {request.method}'
        })
    )


def make_rest(serializer: BaseSerializer, prepare_payload=None):
    
    Model = serializer.model_class()

    def destroy(request, id):
        status = 501 
        result = {
            'message': 'not implemented method'
        }

        try:
            inst = Model.objects.get(pk=id)
            inst.delete()
            status = 204
            result = None
        except Model.DoesNotExist:
            return 404, {
                'message': f'{Model._meta.verbose_name} not found with primary key {id}'
            }
        except Exception as e:
            return 502, {
                'message': str(e)
            }

        return status, result

    def update(request, id):
        status = 501 
        result = {
            'message': 'not implemented method'
        }

        try:
            inst = Model.objects.get(pk=id)
            payload = json.loads(request.body)

            if prepare_payload:
                payload = prepare_payload(request, payload)

            for k, v in payload.items():
                setattr(inst, k, v)

            inst.save()
            status = 200
            result = serializer.encode(inst)
        except Model.DoesNotExist:
            return 404, {
                'message': f'{Model._meta.verbose_name} not found with primary key {id}'
            }
        except Exception as e:
            return 502, {
                'message': str(e)
            }

        return status, result

    def get(request, id):
        try:
            return 200, serializer.encode(Model.objects.get(pk=id))
        except Model.DoesNotExist:
            return 404, {
                'message': f'{Model._meta.verbose_name} not found with primary key {id}'
            }
        except Exception as e:
            return 502, {
                'message': str(e)
            }

    def list(request):
        query = Model.objects.all()
        status = 501
        result = {
            'message': 'not implemented method'
        }

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 30))
        limit = limit if limit < 100 else 100
        total = query.count()

        # filter
        
        # sort

        # page
        start = (page - 1) * limit
        end = page * limit
        query = query[start:end]

        if not query.exists():
            status = 404
            result = {
                'total': 0,
                'offset': {
                    'end': 0,
                    'start': 0,
                },
                'message': f'not found any {Model._meta.verbose_name}'
            }
        else:
            status = 200
            result = {
                'total': total,
                'count': query.count(),
                'offset': {
                    'end': start,
                    'start': end,
                },
                str(Model._meta.verbose_name_plural): [
                    serializer.encode(inst) for inst in query
                ]
            }

        return status, result

    def create(request):
        result = {}
        status = 501

        try:
            payload = json.loads(request.body)
        
            if prepare_payload:
                payload = prepare_payload(request, payload)

            inst = serializer.decode(payload)
            inst.save()

            result = serializer.encode(inst)
            status = 201
        except Exception as e:
            status = 400
            result = {
                "message": str(e)
            }

        return status, result

    def root(request):
        if request.method == 'GET':
            status, result = list(request)

            return JsonResponse(
                result,
                status=status
            )
        elif request.method == 'POST':
            status, result = create(request)

            return JsonResponse(
                result,
                status=status
            )
        else:
            return HttpResponseNotAllowed(
                permitted_methods=['GET', 'POST']
            )

    def by_id(request, id):
        status = 501
        result = {
            "message": "not implemented method"
        }

        if request.method == 'GET':
            status, result = get(request, id)
        elif request.method == 'DELETE':
            status, result = destroy(request, id)
        elif request.method in ('PUT', 'PATCH'):
            status, result = update(request, id)
        else:
            return HttpResponseNotAllowed(
                permitted_methods=['GET', 'PUT', 'PATCH', 'DELETE']
            )

        if isinstance(result, dict):
            return JsonResponse(
                result,
                status=status
            )
        else:
            return HttpResponse(
                status=status,
                content=result if result else ''
            )

    return root, by_id