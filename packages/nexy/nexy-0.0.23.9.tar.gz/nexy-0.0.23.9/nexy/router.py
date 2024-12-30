import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from .utils import deleteFistDotte, dynamicRoute,importModule,convertPathToModulePath
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# 
def FIND_ROUTES(base_path):
    routes:list = []
    
    # Verify if the 'app' folder exists
    if os.path.exists(base_path) and os.path.isdir(base_path):
        # Explore the 'app' folder and its subfolders
        for root, dirs, files in os.walk(base_path):
            #supprimers des _folder
            dirs[:] = [d for d in dirs if not d.startswith("_")]

            route = {
                "pathname": f"{'/' if os.path.basename(root) == base_path else '/' +  deleteFistDotte(os.path.relpath(root, base_path).replace("\\","/"))}",
                "dirName": root
            }
            controller = os.path.join(root, 'controller.py')

            # Check for files and add to dictionary
            if os.path.exists(controller):
                route["module"] = convertPathToModulePath(f"{root}/controller")    

            routes.append(route)

    return routes


env = Environment(loader=FileSystemLoader("app"))   

def render(pathname, data ):
    
    try:
        template = env.get_template(f"{pathname}page.html")
        return template.render(**data)
    
    except TemplateNotFound:
        return HTMLResponse(content=f"Template non trouvé : {pathname}/page.html", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"Erreur lors du rendu du template : {str(e)}", status_code=500)


def Router(appModule: FastAPI, appFolder:str = "app"):
    """
    Charge dynamiquement les routes à partir du répertoire 'app'.
    """
    # Parcours des répertoires dans 'app'
    routes = FIND_ROUTES(base_path=appFolder)
    HTTP_METHODES:tuple = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS")
    for route in routes:

        pathname = dynamicRoute(route_in=route["pathname"])

        if "module" in route:

            module = importModule(path=route["module"])
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Vérifie que l'attribut est une fonction utilisable par FastAPI
                if callable(attr) and hasattr(attr, "__annotations__"):
                    params = getattr(attr, "params", {})
                    

                    # Ajout de la route pour chaque méthode HTTP
                    if attr_name in HTTP_METHODES:
                        
                        if params.get("response_class") == HTMLResponse:
                            appModule.add_api_route(
                                path=pathname,
                                endpoint=lambda:render(pathname,attr()),
                                methods=[attr_name],
                                **params 
                            )
                        else:
                            appModule.add_api_route(
                                path=pathname,
                                endpoint=attr,
                                methods=[attr_name],
                                **params 
                            )

                    # Ajout d'une route WebSocket si la méthode 'Socket' existe
                    if attr_name == "Socket":
                        appModule.add_api_websocket_route(f"{pathname}/ws", attr)



