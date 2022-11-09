import os
import pathlib
import traceback
from importlib import import_module

from ninja import NinjaAPI 
from ninja.errors import AuthenticationError 

from django.conf import settings

api = NinjaAPI(version="1", csrf=True)

@api.exception_handler(AuthenticationError)
def authentication_error(request, exc): 
    return api.create_response(request, {
        "message": str(exc),  
        "tb": traceback.format_exception(exc) if settings.DEBUG else ""
    }, status=401)

@api.exception_handler(Exception) 
def server_error(request, exc): 
    return api.create_response(request, {
        "message": str(exc), 
        "tb": traceback.format_exception(exc) if settings.DEBUG else ""  
    }, status=500)

def init_api_app(api_app): 
    for module in os.listdir(settings.API_PATH): 
        module = pathlib.Path(module) 
        if not module.suffix.endswith('py') or module.stem.startswith('__init__'):  
            continue
        router_module = import_module(f'.{module.stem}') 
        api_app.add_router(f"/{module.stem}", router_module.router)

    return api_app