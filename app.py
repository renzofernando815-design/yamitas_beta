from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import inspect, text
import os
import time
import base64
import io
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///yamitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = int(os.environ.get('REMEMBER_COOKIE_DURATION', 86400 * 30))  # 30 días
app.config['REMEMBER_COOKIE_SECURE'] = os.environ.get('REMEMBER_COOKIE_SECURE', 'False').lower() in ('1', 'true', 'yes')
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'static', 'uploads'))
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.before_request
def serve_uploads():
    pass

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Necesitas iniciar sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

# ==================== MODELOS ====================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tipo_usuario = db.Column(db.String(50), default='comprador')  # comprador, vendedor
    ubicacion = db.Column(db.String(255), nullable=True)  # lugar de producción
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # reproductor, ganador, animal, etc
    foto = db.Column(db.String(255), nullable=True)
    edad = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.String(50), nullable=False)
    tamano = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    numero_servicios = db.Column(db.Integer, nullable=True)
    numero_carabana = db.Column(db.String(100), nullable=True)
    senal = db.Column(db.String(100), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuario = db.relationship('User', backref=db.backref('productos', lazy=True))
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, nullable=False)
    ubicacion = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/static/uploads/<path:filename>')
def serve_upload(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== RUTAS ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        tipo = 'comprador'

        if not username or not email or not password:
            flash('Completa todos los campos para continuar.', 'warning')
            return render_template('registro.html', username=username, email=email)

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return render_template('registro.html', username=username, email=email)

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('registro.html', username=username, email=email)

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'danger')
            return render_template('registro.html', username=username, email=email)

        nuevo_usuario = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            tipo_usuario=tipo
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        usuario = User.query.filter_by(username=username).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario, remember=True)
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('index'))

        flash('Usuario o contraseña inválidos.', 'danger')
        return render_template('login.html', username=username)
    
    return render_template('login.html')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/editar-ubicacion', methods=['POST'])
@login_required
def editar_ubicacion():
    ubicacion = request.form.get('ubicacion', '').strip()
    
    if not ubicacion:
        flash('La ubicación no puede estar vacía.', 'warning')
        return redirect(url_for('perfil'))
    
    if len(ubicacion) > 255:
        flash('La ubicación no puede exceder 255 caracteres.', 'danger')
        return redirect(url_for('perfil'))
    
    current_user.ubicacion = ubicacion
    db.session.commit()
    flash('Ubicación actualizada correctamente.', 'success')
    return redirect(url_for('perfil'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def normalize_foto_path(foto_path):
    """Normaliza la ruta de la foto a usar siempre /"""
    if foto_path:
        return foto_path.replace('\\', '/')
    return foto_path


def ensure_producto_columns():
    inspector = inspect(db.engine)
    if 'producto' not in inspector.get_table_names():
        return

    existing = {col['name'] for col in inspector.get_columns('producto')}
    migrations = []

    if 'foto' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN foto VARCHAR(255)")
    if 'edad' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN edad VARCHAR(50) DEFAULT ''")
    if 'peso' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN peso VARCHAR(50) DEFAULT ''")
    if 'tamano' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN tamano VARCHAR(50) DEFAULT ''")
    if 'raza' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN raza VARCHAR(100) DEFAULT ''")
    if 'color' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN color VARCHAR(100) DEFAULT ''")
    if 'numero_servicios' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN numero_servicios INTEGER")
    if 'numero_carabana' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN numero_carabana VARCHAR(100)")
    if 'senal' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN senal VARCHAR(100)")
    if 'usuario_id' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN usuario_id INTEGER")
    if 'fecha_creacion' not in existing:
        migrations.append("ALTER TABLE producto ADD COLUMN fecha_creacion DATETIME")

    if migrations:
        with db.engine.connect() as conn:
            for statement in migrations:
                conn.execute(text(statement))
            conn.commit()

@app.route('/publicar', methods=['GET', 'POST'])
@login_required
def publicar():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', '').strip()
        edad = request.form.get('edad', '').strip()
        peso = request.form.get('peso', '').strip()
        tamano = request.form.get('tamano', '').strip()
        raza = request.form.get('raza', '').strip()
        color = request.form.get('color', '').strip()
        numero_servicios = request.form.get('numero_servicios', '').strip()
        numero_carabana = request.form.get('numero_carabana', '').strip()
        senal = request.form.get('senal', '').strip()
        tipo = 'reproductor'

        ensure_producto_columns()
        
        # Procesar imagen: puede venir como archivo o como base64
        foto_ruta = None
        foto_base64 = request.form.get('foto', '').strip()
        foto = request.files.get('foto')
        
        if foto_base64 and foto_base64.startswith('data:image'):
            # Procesar imagen base64 (recortada)
            try:
                # Extraer el base64 del data URL
                header, encoded = foto_base64.split(',', 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
                
                # Generar nombre de archivo
                filename = f"{current_user.id}_{int(time.time())}_cropped.jpg"
                destino = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Guardar como JPEG optimizado
                image.convert('RGB').save(destino, 'JPEG', quality=85, optimize=True)
                foto_ruta = f"uploads/{filename}"
            except Exception as e:
                flash(f'Error al procesar la imagen: {str(e)}', 'danger')
                return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                       edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                       numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)
        elif foto and foto.filename != '':
            # Procesar archivo tradicional
            if not allowed_file(foto.filename):
                flash('El archivo de imagen debe ser PNG, JPG, JPEG o GIF.', 'danger')
                return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                       edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                       numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)
            
            filename = secure_filename(foto.filename)
            timestamp = int(time.time())
            filename = f"{current_user.id}_{timestamp}_{filename}"
            destino = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(destino)
            foto_ruta = f"uploads/{filename}"
        
        if not foto_ruta:
            flash('Debes seleccionar y recortar una foto del animal.', 'warning')
            return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            precio_valor = int(precio)
            if precio_valor < 10000 or precio_valor > 999999:
                raise ValueError()
        except ValueError:
            flash('Ingresa un precio entero de 5 a 6 dígitos.', 'danger')
            return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            edad_valor = int(edad)
            if edad_valor < 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa una edad numérica válida.', 'danger')
            return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            peso_valor = float(peso)
            if peso_valor <= 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa un peso numérico válido.', 'danger')
            return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            tamano_valor = float(tamano)
            if tamano_valor <= 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa un tamaño numérico válido.', 'danger')
            return render_template('publicar.html', nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        servicios_valor = None
        if numero_servicios.isdigit():
            servicios_valor = int(numero_servicios)

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio_valor,
            tipo=tipo,
            foto=foto_ruta,
            edad=str(edad_valor),
            peso=str(peso_valor),
            tamano=str(tamano_valor),
            raza=raza,
            color=color,
            numero_servicios=servicios_valor,
            numero_carabana=numero_carabana or None,
            senal=senal or None,
            usuario_id=current_user.id
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        flash('Animal publicado correctamente.', 'success')
        return redirect(url_for('publicar'))

    return render_template('publicar.html')

@app.route('/ferias')
def ferias():
    eventos = Evento.query.all()
    return render_template('ferias.html', eventos=eventos)

@app.route('/reproductores')
def reproductores():
    productos = Producto.query.filter_by(tipo='reproductor').all()
    return render_template('productos.html', productos=productos, titulo='Reproductores en Venta')

@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return render_template('producto_detalle.html', producto=producto)

@app.route('/producto/<int:producto_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    if producto.usuario_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', '').strip()
        edad = request.form.get('edad', '').strip()
        peso = request.form.get('peso', '').strip()
        tamano = request.form.get('tamano', '').strip()
        raza = request.form.get('raza', '').strip()
        color = request.form.get('color', '').strip()
        numero_servicios = request.form.get('numero_servicios', '').strip()
        numero_carabana = request.form.get('numero_carabana', '').strip()
        senal = request.form.get('senal', '').strip()

        if not nombre or not precio or not edad or not peso or not tamano or not raza or not color:
            flash('Completa todos los campos obligatorios.', 'warning')
            return render_template('editar_producto.html', producto=producto,
                                   nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        foto = request.files.get('foto')
        foto_base64 = request.form.get('foto', '').strip()
        
        if foto_base64 and foto_base64.startswith('data:image'):
            # Procesar imagen base64 (recortada)
            try:
                # Extraer el base64 del data URL
                header, encoded = foto_base64.split(',', 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
                
                # Generar nombre de archivo
                filename = f"{current_user.id}_{int(time.time())}_cropped.jpg"
                destino = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Guardar como JPEG optimizado
                image.convert('RGB').save(destino, 'JPEG', quality=85, optimize=True)
                producto.foto = f"uploads/{filename}"
            except Exception as e:
                flash(f'Error al procesar la imagen: {str(e)}', 'danger')
                return render_template('editar_producto.html', producto=producto,
                                       nombre=nombre, descripcion=descripcion, precio=precio,
                                       edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                       numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)
        elif foto and foto.filename != '':
            # Procesar archivo tradicional
            if not allowed_file(foto.filename):
                flash('El archivo de imagen debe ser PNG, JPG, JPEG o GIF.', 'danger')
                return render_template('editar_producto.html', producto=producto,
                                       nombre=nombre, descripcion=descripcion, precio=precio,
                                       edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                       numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)
            filename = secure_filename(foto.filename)
            timestamp = int(time.time())
            filename = f"{current_user.id}_{timestamp}_{filename}"
            destino = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(destino)
            producto.foto = f"uploads/{filename}"

        try:
            precio_valor = int(precio)
            if precio_valor < 10000 or precio_valor > 999999:
                raise ValueError()
        except ValueError:
            flash('Ingresa un precio entero de 5 a 6 dígitos.', 'danger')
            return render_template('editar_producto.html', producto=producto,
                                   nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            edad_valor = int(edad)
            if edad_valor < 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa una edad numérica válida.', 'danger')
            return render_template('editar_producto.html', producto=producto,
                                   nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            peso_valor = float(peso)
            if peso_valor <= 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa un peso numérico válido.', 'danger')
            return render_template('editar_producto.html', producto=producto,
                                   nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        try:
            tamano_valor = float(tamano)
            if tamano_valor <= 0:
                raise ValueError()
        except ValueError:
            flash('Ingresa un tamaño numérico válido.', 'danger')
            return render_template('editar_producto.html', producto=producto,
                                   nombre=nombre, descripcion=descripcion, precio=precio,
                                   edad=edad, peso=peso, tamano=tamano, raza=raza, color=color,
                                   numero_servicios=numero_servicios, numero_carabana=numero_carabana, senal=senal)

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio_valor
        producto.edad = str(edad_valor)
        producto.peso = str(peso_valor)
        producto.tamano = str(tamano_valor)
        producto.raza = raza
        producto.color = color
        producto.numero_servicios = int(numero_servicios) if numero_servicios.isdigit() else None
        producto.numero_carabana = numero_carabana or None
        producto.senal = senal or None

        db.session.commit()
        flash('Animal actualizado correctamente.', 'success')
        return redirect(url_for('detalle_producto', producto_id=producto.id))

    return render_template('editar_producto.html', producto=producto)

@app.route('/ganadores')
def ganadores():
    productos = Producto.query.filter_by(tipo='ganador').all()
    return render_template('productos.html', productos=productos, titulo='Ganadores y Resultados')

@app.route('/productores')
def productores():
    usuarios = User.query.filter_by(tipo_usuario='vendedor').all()
    return render_template('productores.html', productores=usuarios)

@app.route('/consejos')
def consejos():
    return render_template('consejos.html')

@app.route('/asistente-ia')
def asistente_ia():
    return render_template('asistente_ia.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_producto_columns()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    )
