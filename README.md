# Yamitas

Aplicación Flask para publicar animales, noticias de ferias y gestionar usuarios.

## Contenido del repositorio
- `app.py`: aplicación principal Flask
- `requirements.txt`: dependencias de Python
- `templates/`: vistas HTML
- `static/`: CSS, JS, imágenes y archivos subidos
- `fix_paths.py`: script de limpieza de rutas de imágenes en la base de datos

## Configuración local
1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
2. Activar el entorno:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows CMD:
     ```cmd
     .\venv\Scripts\activate
     ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la app:
   ```bash
   python app.py
   ```
5. Abrir `http://127.0.0.1:5000` en el navegador.

## GitHub
1. Inicializar el repositorio local:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Crear un repositorio nuevo en GitHub.
3. Conectar el repositorio remoto y enviar los cambios:
   ```bash
   git remote add origin https://github.com/<usuario>/<repositorio>.git
   git branch -M main
   git push -u origin main
   ```

## Sobre Netlify
Netlify está diseñado principalmente para sitios estáticos y funciones sin servidor. Esta aplicación es una app Flask con backend Python y SQLite, por lo que no se puede desplegar directamente como un sitio completo en Netlify.

### Opciones recomendadas
- Desplegar la app Flask completa en un servicio Python como Render, Railway, PythonAnywhere o Heroku.
- Si deseas usar Netlify, genera una versión estática del frontend con `python build_static.py` y mantén el backend Flask en otro servicio.

## Despliegue en Netlify (estático)
1. Instala dependencias localmente o en el servidor de compilación:
   ```bash
   pip install -r requirements.txt
   ```
2. Genera el sitio estático:
   ```bash
   python build_static.py
   ```
3. Despliega el contenido de la carpeta `public/` en Netlify.

> Ten en cuenta que esta versión estática no conserva el inicio de sesión ni el almacenamiento SQLite ni las funciones de publicación/edición.

## Notas
- El archivo `app.py` ahora usa variables de entorno para `SECRET_KEY`, `DATABASE_URL` y configuración de cookies, lo que facilita el despliegue en servicios Python.
- El archivo `build_static.py` genera una versión estática de las páginas principales para Netlify.
- Asegúrate de no subir datos personales ni archivos subidos de usuarios al repositorio.
