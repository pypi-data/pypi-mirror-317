
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json


from .forthright_server import g_exported_functions_dict, unserialize_arguments_server, serialize_arguments, \
                                g_safe_mode, MyJsonEncoder, specify_type_hook


@api_view(['PUT'])
def get_data(request):


    global g_exported_functions_dict
    global g_safe_mode

    data = request.body

    if g_safe_mode:
        unserialized = json.loads(data, object_hook=specify_type_hook)
    else:
        unserialized = unserialize_arguments_server(data)


    function_name = unserialized[0]
    input_kwargs = unserialized[1]
    input_args = unserialized[2:]

    try:
        outputs = g_exported_functions_dict[function_name](*input_args, **input_kwargs)
    except KeyError:
        raise KeyError('forthright: %s() not found. Use forthright_server.export_functions(%s)' %(function_name, function_name))


    if g_safe_mode:
        json_encoder = MyJsonEncoder()
        content_type = 'application/json'
        outputs_serialized = json_encoder.encode(outputs)
    else:
        content_type = 'application/octet-stream'
        outputs_serialized = serialize_arguments(outputs)

    return HttpResponse(outputs_serialized, content_type=content_type)




