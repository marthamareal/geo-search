import itertools

from rest_framework.exceptions import ValidationError

from api.location.models import OPERATION_TYPE_CHOICES


def validate_float(key, value):
    try:
        return float(value)
    except:
        raise ValidationError(
            {'error': '%s must be of type float.' % key}
        )


def validated_request_params(request):
    if ['x', 'y', 'n', 'operation_type'].sort() == list(request.GET.keys()).sort():
        x = validate_float('x', request.GET.get('x'))
        y = validate_float('y', request.GET.get('y'))
        n = request.GET.get('n')
        operation_type = request.GET.get('operation_type')
        # validate n and operation_type
        try:
            n = int(n)
        except:
            raise ValidationError(
                {'error': 'n must be of type int.'}
            )
        if operation_type not in itertools.chain(*OPERATION_TYPE_CHOICES):
            raise ValidationError(
                {'error': 'operation_type must either be nearest or furthest'}
            )
        return {
            'x': x,
            'y': y,
            'n': n,
            'operation_type': operation_type
        }
    raise ValidationError(
        {'error': 'All params x, y, n and operation_type are required'}
    )
