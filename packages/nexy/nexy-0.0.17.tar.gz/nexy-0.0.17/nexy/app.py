from fastapi import FastAPI
from .router import Router
import sys
from pathlib import Path


def Nexy(title: str = None ,**args):
    if title is None:
        title = Path.cwd().name 

    app:FastAPI = FastAPI(title=title,**args)

    # Configurer le cache
    cache_dir = Path('./__pycache__/nexy')
    cache_dir.mkdir(exist_ok=True)
    sys.pycache_prefix = str(cache_dir)

    Router(appModule=app)
    return app

