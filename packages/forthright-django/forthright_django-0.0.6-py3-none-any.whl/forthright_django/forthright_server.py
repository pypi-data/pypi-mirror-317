
import pickle
import inspect
import json
import base64



# Hold on to the name of the module which instantiated the forthright_server object
# because this is where the class definition should be located when unserializing custom objects
g_caller_module_name = ''

g_exported_functions_dict = {}

g_safe_mode = False


# https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json
class MyJsonEncoder(json.JSONEncoder):
    def encode(self, obj):
        def specify_type(item):
            if isinstance(item, tuple):
                return {'__tuple__': True, 'items': [specify_type(e) for e in item]}
            elif isinstance(item, set):
                return {'__set__': True, 'items': [specify_type(e) for e in item]}
            elif isinstance(item, bytes):
                return {'__bytes__': True, 'items': base64.b64encode(item).decode('utf8')}
            elif isinstance(item, list):
                return [specify_type(e) for e in item]
            elif isinstance(item, dict):
                return {key: specify_type(value) for key, value in item.items()}
            else:
                return item

        return super(MyJsonEncoder, self).encode(specify_type(obj))


def specify_type_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    elif '__set__' in obj:
        return set(obj['items'])
    elif '__bytes__' in obj:
        return base64.b64decode(obj['items'])
    else:
        return obj



# https://stackoverflow.com/questions/50465106/attributeerror-when-reading-a-pickle-file
class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):

        # If there's a custom object in the bytes_stream, 
        # change the module name to the name of the module that instantiated this forthright_server object
        # because that's where the class should be defined

        global g_caller_module_name

        module_name = g_caller_module_name

        try:
            # try same module as sender (works for numpy)
            return super().find_class(module, name)
        except:
            # try module in which forthright was instantiated (works for custom class)
            return super().find_class(module_name, name)


def serialize_arguments(*args):

    args_tuple = tuple(args)
    args_serialized = pickle.dumps(args_tuple)

    return args_serialized

def unserialize_arguments_server(args_serialized):

    import io
    bytes_stream = io.BytesIO(args_serialized)

    unpickler = MyCustomUnpickler(bytes_stream)
    args_tuple = unpickler.load()

    return args_tuple



class forthright_server:
    def __init__(self, safe_mode=False):
        self.exported_functions_dict = {}
        self.safe_mode = safe_mode

        global g_safe_mode
        g_safe_mode = self.safe_mode

        # Get module name of caller
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__

        global g_caller_module_name
        g_caller_module_name = module_name


    def register_functions(self, *funcs):

        global g_exported_functions_dict

        for func in funcs:
            self.exported_functions_dict[func.__name__] = func

        g_exported_functions_dict = self.exported_functions_dict



