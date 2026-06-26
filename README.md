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

## Versión de Python
- El proyecto fue probado localmente con Python 3.14.5.
- Si usas un host Python, ajusta `runtime.txt` o la configuración del servicio según la versión admitida.

## Instalar Ollama
1. Instala Ollama en tu máquina siguiendo las instrucciones oficiales: https://ollama.ai
2. Si Ollama no está en el PATH o usas Windows, define la variable de entorno `OLLAMA_COMMAND` con la ruta completa al ejecutable.
   - PowerShell (solo para la sesión actual):
     ```powershell
     $env:OLLAMA_COMMAND = 'C:\Program Files\Ollama\ollama.exe'
     ```
   - Windows (persistente):
     ```powershell
     setx OLLAMA_COMMAND 'C:\Program Files\Ollama\ollama.exe'
     ```
   - Linux/macOS:
     ```bash
     export OLLAMA_COMMAND='/usr/local/bin/ollama'
     ```
3. (Opcional) Si quieres usar otro modelo, define `OLLAMA_MODEL`:
   ```bash
   export OLLAMA_MODEL='mistral'
   ```
4. Ejecuta la aplicación de Flask y entra en `/asistente-ia`.

> Nota: este repositorio incluye `check_ollama.py` para verificar que Ollama esté instalado y que los modelos estén disponibles.

## Verificar Ollama localmente
1. Ejecuta el script de verificación:
   ```bash
   python check_ollama.py
   ```
2. Si el script encuentra Ollama y modelos instalados, verás la ruta y la lista de modelos.
3. Si no encuentra el ejecutable, revisa `OLLAMA_COMMAND`.
4. Para instalar el modelo predeterminado `mistral`:
   ```bash
   ollama pull mistral
   ```

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

## Despliegue en Vercel (estático)
Esta configuración genera un sitio estático en `public/` usando `build_static.py`.

1. Instala dependencias localmente o en el servidor de compilación:
   ```bash
   pip install -r requirements.txt
   ```
2. Genera el sitio estático:
   ```bash
   python build_static.py
   ```
3. En Vercel, el build command es:
   ```bash
   npm run build
   ```
4. El directorio de salida es:
   ```bash
   public
   ```
5. El proyecto ya incluye los archivos de Vercel:
   - `vercel.json`
   - `package.json`

> El sitio exportado es estático. No conserva inicio de sesión, bases de datos SQLite, ni las funciones dinámicas de publicación, edición, login o búsqueda en servidor.
> El backend Flask completo no se ejecuta en este despliegue estático.
> `build_static.py` usa un usuario ficticio y un estado de Ollama por defecto para poder renderizar las páginas sin la infraestructura dinámica.

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
> Esta configuración está preparada para Python 3.11.4 en Netlify.
## Notas
- El archivo `app.py` ahora usa variables de entorno para `SECRET_KEY`, `DATABASE_URL` y configuración de cookies, lo que facilita el despliegue en servicios Python.
- El archivo `build_static.py` genera una versión estática de las páginas principales para Vercel/Netlify y ya incluye valores predeterminados para `current_user` y `ollama_status`.
- Se agregó el endpoint `/productores/<int:user_id>` (`productor_venta`) para permitir la navegación entre productores y sus productos.
- Asegúrate de no subir datos personales ni archivos subidos de usuarios al repositorio.
