import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

TEMPLATE_DIR = os.path.join(os.getcwd(), "templates")

template_engine = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True
)

def render_template(template_name: str, context=None) -> bytes:
    context = context or {}
    try:
        tmpl = template_engine.get_template(template_name)
        return tmpl.render(context).encode("utf-8")
    except TemplateNotFound:
        raise FileNotFoundError(f"Template '{template_name}' not found in '{TEMPLATE_DIR}'")
