from fastapi.responses import  HTMLResponse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from nexy.utils import find_page_html

def useView(data):
    path = find_page_html()
    env = Environment(loader=FileSystemLoader("app"))   
    
    try:
        template = env.get_template(path)
        return template.render(data)
    
    except TemplateNotFound:
        return HTMLResponse(content=f"Template non trouvé : {path}/page.html", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"Erreur lors du rendu du template : {str(e)}", status_code=500)

