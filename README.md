Instrucciones sencillitas:
   Una vez abre el repositorio que contiene todo el codigo se va a   <>code
   y le da a 'dowloand zip'

una vez que tenga descargado el zip, lo descomprime en alguna carpeta
con eso ya tendria el proyecto en su compu

-si quiere abrirlo y solo ver EL CODIGO
   vaya a https://vscode.dev/?vscode-lang=es-419 para no tener que descargar nada
   una vez en la pagina le da a 'abrir carpeta' y selecciona la del proyecto

-si quiere ejecutarlo:
  1) descarga visual studio code y creo que le pide crearse una cuenta (creo)
   2) selecciona la carpeta del proyecto
   3) una vez abierta la carpeta del proyecto debe abrir una nueva terminal (apartado superior izquierdo)
   4) lo primero que debe escribir es  (esto instalara los requerimientos)
   ```bash
   pip install -r requirements.txt
   ```
   5) da inicio al proyecto con
   ```bash
   python app.py
   ```
   6) abre chrome o su navegador web y copia `http://127.0.0.1:5000` en la URL

<<<<<<< HEAD
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
=======
el proyecto cuenta con un par de anotaciones para que se pueda guiar un poco de que es cada seccion del codigo pero en resumen
app.py es la base
en la carpeta 'templates' estan los htmls de cada pagina que se muestra en la app
eso creo que es todo, si me olvido algo pido disculpas

No me robe el codigo profe -_-
>>>>>>> e7c98887bbb8118841be6c5fc0f2b57467273d44
