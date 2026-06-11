#!/usr/bin/env python3
"""Script para corregir las rutas de las fotos en la base de datos"""

from app import app, db, Producto
import os

def fix_foto_paths():
    with app.app_context():
        productos = Producto.query.all()
        fixed_count = 0
        
        for producto in productos:
            if producto.foto:
                original_foto = producto.foto
                # Normalizar la ruta: reemplazar backslashes con forward slashes
                normalized = producto.foto.replace('\\', '/')
                
                # Eliminar duplicaciones de "uploads/"
                while 'uploads//uploads/' in normalized:
                    normalized = normalized.replace('uploads//uploads/', 'uploads/')
                while 'uploads/uploads/' in normalized:
                    normalized = normalized.replace('uploads/uploads/', 'uploads/')
                
                # Asegurar que comience con "uploads/"
                if not normalized.startswith('uploads/'):
                    # Extraer solo el nombre del archivo
                    filename = os.path.basename(normalized)
                    normalized = f'uploads/{filename}'
                
                if original_foto != normalized:
                    print(f"Corrigiendo: {original_foto} -> {normalized}")
                    producto.foto = normalized
                    fixed_count += 1
        
        if fixed_count > 0:
            db.session.commit()
            print(f"\n✓ Se corrigieron {fixed_count} productos")
        else:
            print("No hay productos con rutas incorrectas")

if __name__ == '__main__':
    fix_foto_paths()
