from fastapi import FastAPI
from fastapi.responses import FileResponse
from .router import Router
import sys
from pathlib import Path


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

