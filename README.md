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
Netlify está diseñado principalmente para sitios estáticos y funciones sin servidor. Esta aplicación es una app Flask con backend Python y SQLite, por lo que no se puede desplegar directamente como un sitio estático de Netlify.

### Opciones recomendadas
- Desplegar la app Flask completa en un servicio Python como Render, Railway, PythonAnywhere o Heroku.
- Si deseas usar Netlify, separa el frontend estático y usa un backend Flask independiente en otro servicio.

## Notas
- El archivo `app.py` crea la base de datos local y aplica migraciones simples al iniciar.
- Asegúrate de no subir datos personales ni archivos subidos de usuarios al repositorio.
