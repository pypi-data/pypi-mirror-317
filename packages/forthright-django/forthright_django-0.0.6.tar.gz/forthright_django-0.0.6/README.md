
# forthright-django


forthright-django is a Django app to allow developers to directly call server functions from the client. 

## Quick start

1. `pip install forthright-django`


2. Add forthright-django to INSTALLED_APPS in your django project settings.py:

    ```
    INSTALLED_APPS = [
        ...,
        'forthright_django',
    ]
    ```

3. Include the forthright-django URLconf in your django project urls.py:

    ```
    urlpatterns = [
        path('forthright/', include('forthright_django.urls')),
        ...,
    ]
    ```

4. Instantiate a forthright_server object and export your server functions. For example, place [examples/server_functions.py](./examples/server_functions.py) in your django project folder, and import this file in urls.py

    `from . import server_functions`


5. Now you can instantiate a forthright_client object on the client and directly call the server functions that you exported. For example, [examples/client.py](./examples/client.py)


All together, here's an example django project:

<div float="left">
    <img src="./examples/example_django_project.png" alt="example_django_project" height="400">
</div>
<br>

And corresponding client:

<div float="left">
    <img src="./examples/example_client.png" alt="example_client" height="133">
</div>
<br>


## Limitations

You can only pass arguments by value, not by reference. For example, if an argument is a list, the server function will receive a copy of that list.

If an argument is a custom object, the class definition must be present in both the client code and the server code.

Warning: By default, this code deserializes pickled data on the server which is unsafe. There is an optional Safe Mode to instead send data with json, but this will prevent you from sending custom objects. To turn on Safe Mode, set `safe_mode=True` when instantiating both forthright_server and forthright_client:

`frs = forthright_server(safe_mode=True)`

`frc = forthright_client(url, safe_mode=True)`



