import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .utils import deleteFistDotte, dynamicRoute,importModule,convertPathToModulePath

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




def Router(appModule: FastAPI, appFolder:str = "app"):
    """
    Charge dynamiquement les routes à partir du répertoire 'app'.
    """
    # Parcours des répertoires dans 'app'
    routes = FIND_ROUTES(base_path=appFolder);
    HTTP_METHODES:tuple = ("GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS");
    for route in routes:

        pathname = dynamicRoute(route_in=route["pathname"]);

        if "module" in route:

            module = importModule(path=route["module"]);
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Vérifie que l'attribut est une fonction utilisable par FastAPI
                if callable(attr) and hasattr(attr, "__annotations__"):
                    params = getattr(attr, "params", {})
                    # Ajout de la route pour chaque méthode HTTP
                    if attr_name in HTTP_METHODES:
                        
                        method = attr_name
                        appModule.add_api_route(
                            path=pathname,
                            endpoint=attr,
                            methods=[method],
                            response_model=params.get("response_model", None),
                            status_code=params.get("status_code", 200),
                            tags=params.get("tags", None),
                            summary=params.get("summary", None),
                            description=params.get("description", None),
                            response_description=params.get("response_description", "Successful Response"),
                            responses=params.get("responses", None),
                            dependencies=params.get("dependencies", None),
                            deprecated=params.get("deprecated", None),
                            operation_id=params.get("operation_id", None),
                            response_model_include=params.get("response_model_include", None),
                            response_model_exclude=params.get("response_model_exclude", None),
                            response_model_by_alias=params.get("response_model_by_alias", True),
                            response_model_exclude_unset=params.get("response_model_exclude_unset", False),
                            response_model_exclude_defaults=params.get("response_model_exclude_defaults", False),
                            response_model_exclude_none=params.get("response_model_exclude_none", False),
                            include_in_schema=params.get("include_in_schema", True),
                            response_class=params.get("response_class", JSONResponse),  # Supposons que JSONResponse est ton param par défaut
                            name=params.get("name", None),
                            openapi_extra=params.get("openapi_extra", None),
                            generate_unique_id_function=params.get("generate_unique_id_function", None)
                           
                        )

                       
                    # Ajout d'une route WebSocket si la méthode 'Socket' existe
                    if attr_name == "Socket":
                        appModule.add_api_websocket(f"{pathname}/ws", attr)
                        appModule.websocket()



