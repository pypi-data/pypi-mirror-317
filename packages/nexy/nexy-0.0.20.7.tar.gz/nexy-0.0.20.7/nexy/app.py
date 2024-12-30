from fastapi import FastAPI,Response, Depends
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.responses import FileResponse,JSONResponse
from fastapi.types import IncEx
from .router import Router
import sys
from pathlib import Path
from typing import Any, List, Dict, Sequence, Type
from functools import wraps


def Nexy(title: str = None ,**args):
    if title is None:
        title = Path.cwd().name 

    app:FastAPI = FastAPI(title=title,**args)
    
    @app.get("/{name}/{file_path:path}")
    async def serve_static_files(name: str, file_path: str):
        # Construire le chemin complet vers le fichier dans le dossier public
        file_location = Path(f"public/{name}/{file_path}")
        
        # Vérifier si le fichier existe
        if file_location.is_file():
            return FileResponse(file_location)
        else:
            return {"error": "File not found"}

    # Configurer le cache
    cache_dir = Path('./__pycache__/nexy')
    cache_dir.mkdir(exist_ok=True)
    sys.pycache_prefix = str(cache_dir)

    Router(appModule=app)
    return app


# Définir le décorateur Params avec tous les paramètres fournis
def Params(
    *,
    response_model: Any = Default(None),
    status_code: int | None = None,
    tags: List[str] | None = None,
    dependencies: Sequence[Depends] | None = None,
    summary: str | None = None,
    description: str | None = None,
    response_description: str = "Successful Response",
    responses: Dict[int | str, Dict[str, Any]] | None = None,
    deprecated: bool | None = None,
    operation_id: str | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Type[Response] | DefaultPlaceholder = Default(JSONResponse),
    name: str | None = None,
    openapi_extra: Dict[str, Any] | None = None,
):
    """
    Un décorateur pour ajouter des paramètres personnalisés à une route.
    """
    
    def decorator(func):
        # Dictionnaire pour stocker les paramètres
        func.params = {}

        # Ajout des paramètres seulement s'ils ne sont pas None ou la valeur par défaut
        for param, value in locals().items():
            if param != "func" and value is not None and not isinstance(value, Default):
                func.params[param] = value

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Appeler la fonction originale et obtenir son résultat
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

