
import os
import shutil
import json
from datetime import datetime
from urllib.parse import urlparse
from app import app, User, db
from flask import render_template
from sqlalchemy.orm import joinedload


class DummyObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def render_page(template_name, output_path, context):
    output_file = os.path.join(PUBLIC_DIR, output_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with app.test_request_context('/'):
        # When exporting static pages (for Vercel/Netlify), avoid showing
        # runtime warnings about Ollama not being available. Provide a
        # neutral `ollama_status` that prevents the template from showing
        # error banners in the static build.
        default_ollama_status = {
            'ollama_command': '',
            'ollama_available': True,
            'installed_models': [],
            'requested_model': getattr(app, 'OLLAMA_MODEL', 'mistral'),
            'resolved_model': getattr(app, 'OLLAMA_MODEL', 'mistral'),
            'model_installed': True,
        }

        page_context = {
            'current_user': app.jinja_env.globals.get('current_user'),
            'ollama_status': default_ollama_status,
            'news_items': context.get('news_items', []),
            **context,
        }
        html = render_template(template_name, **page_context)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)


def create_public_directory():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    source_static = os.path.join(ROOT_DIR, 'static')
    destination_static = os.path.join(PUBLIC_DIR, 'static')
    shutil.copytree(source_static, destination_static, dirs_exist_ok=True)


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')


def get_productores():
    try:
        with app.app_context():
            return User.query.options(joinedload(User.productos)).all()
    except Exception:
        return []


def get_static_news_items():
    news_items = []
    json_path = os.path.join(ROOT_DIR, 'news_sources.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            urls = data.get('urls', []) if isinstance(data, dict) else data
            urls = [u.strip() for u in urls if isinstance(u, str) and u.strip()]

        for index, url in enumerate(urls[:5]):
            news_items.append({
                'id': f'placeholder-{index}',
                'url': url,
                'title': f'Cargando noticias de {urlparse(url).hostname or url}...',
                'is_global': True,
                'placeholder': True,
            })
    except Exception:
        pass

    return news_items


def main():
    create_public_directory()

    dummy_user = DummyObject(
        is_authenticated=False,
        username='Invitado',
        email='usuario@ejemplo.com',
        fecha_registro=datetime.now(),
        ubicacion='Sin ubicación'
    )

    app.jinja_env.globals['current_user'] = dummy_user

    dummy_usuario = DummyObject(username='Productor Demo', ubicacion='Abra Pampa')
    dummy_producto = DummyObject(
        id=1,
        nombre='Ejemplo de producto',
        descripcion='Descripción de ejemplo para el export estático. Este contenido es solo de muestra.',
        precio=125000.00,
        tipo='reproductor',
        foto='icons/app-icon-192.png',
        edad='3',
        peso='55',
        tamano='1.5',
        raza='Tampulli',
        color='Blanco',
        numero_servicios=2,
        numero_carabana='12345',
        senal='Marca blanca',
        usuario_id=1,
        usuario=dummy_usuario,
        fecha_creacion=datetime.now()
    )

    pages = [
        {'template': 'index.html', 'output': 'index.html', 'context': {'news_items': get_static_news_items()}},
        {'template': 'registro.html', 'output': os.path.join('registro', 'index.html'), 'context': {}},
        {'template': 'login.html', 'output': os.path.join('login', 'index.html'), 'context': {}},
        {'template': 'perfil.html', 'output': os.path.join('perfil', 'index.html'), 'context': {}},
        {'template': 'publicar.html', 'output': os.path.join('publicar', 'index.html'), 'context': {'nombre': '', 'precio': '', 'descripcion': '', 'edad': '', 'peso': '', 'tamano': '', 'raza': '', 'color': '', 'numero_servicios': '', 'numero_carabana': '', 'senal': ''}},
        {'template': 'ferias.html', 'output': os.path.join('ferias', 'index.html'), 'context': {
            'eventos': [],
            'eventos_json': [],
            'authenticated': False,
            'min_date': datetime.now().date().isoformat()
        }},
        {'template': 'productos.html', 'output': os.path.join('reproductores', 'index.html'), 'context': {'productos': [], 'titulo': 'Reproductores en Venta'}},
        {'template': 'productos.html', 'output': os.path.join('ganadores', 'index.html'), 'context': {'productos': [], 'titulo': 'Ganadores y Resultados'}},
        {'template': 'productores.html', 'output': os.path.join('productores', 'index.html'), 'context': {'productores': get_productores()}},
        {'template': 'consejos.html', 'output': os.path.join('consejos', 'index.html'), 'context': {}},
        {'template': 'asistente_ia.html', 'output': os.path.join('asistente-ia', 'index.html'), 'context': {}},
        {'template': 'producto_detalle.html', 'output': os.path.join('producto', '1', 'index.html'), 'context': {'producto': dummy_producto}},
        {'template': 'editar_producto.html', 'output': os.path.join('producto', '1', 'editar', 'index.html'), 'context': {'producto': dummy_producto}},
    ]

    for page in pages:
        render_page(page['template'], page['output'], page['context'])

    print(f'Static site written to: {PUBLIC_DIR}')


if __name__ == '__main__':
    main()
