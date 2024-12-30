import os
import re
import importlib
# 
def deleteFistDotte(string:str)-> str:
    if string.startswith('.'):
        return re.sub(r'^.', '', string)
    else:
        return string
    
def dynamicRoute(route_in:str)-> str:

    # Remplacer [id] par {id}
    route_out = re.sub(r"\[([^\]]+)\]", r"{\1}",route_in)
    # Remplacer {_slug} par {slug:path} pour capturer plusieurs segments
    route_out = re.sub(r"\{_([^\}]+)\}", r"{\1}:path", route_out)

    return route_out

def convertPathToModulePath(path:str)->str:
    return re.sub(r"\\|/", ".", path)

def importModule(path:str):
    try:
        module =importlib.import_module(path) 
    except ModuleNotFoundError as e:
        print(f"Error importing module '{path}': {e}")
    return module



def find_page_html():
    # Récupérer le chemin du module actuel (fichier Python qui appelle cette fonction)
    current_module_path = os.path.dirname(os.path.abspath(__file__))  # __file__ donne le fichier actuel

    # Chercher page.html dans le même répertoire que le module
    page_html_path = os.path.join(current_module_path, 'page.html')

    # Vérifier si le fichier existe
    if os.path.exists(page_html_path):
        return page_html_path
    else:
        return None 