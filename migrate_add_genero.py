#!/usr/bin/env python
# Script para agregar la columna 'genero' a la tabla 'animal'

import os
import sys
from app import app, db, Animal
from sqlalchemy import inspect, text

def migrate_add_genero():
    """Agregar columna genero a la tabla animal si no existe"""
    with app.app_context():
        try:
            # Verificar si la columna genero ya existe
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('animal')]
            
            if 'genero' in columns:
                print("✓ La columna 'genero' ya existe en la tabla 'animal'")
                return True
            
            # Agregar la columna
            with db.engine.begin() as connection:
                connection.execute(text('ALTER TABLE animal ADD COLUMN genero VARCHAR(50)'))
                print("✓ Columna 'genero' agregada exitosamente a la tabla 'animal'")
            
            # Establecer valores por defecto para registros existentes
            with db.engine.begin() as connection:
                connection.execute(text("UPDATE animal SET genero = 'Macho' WHERE genero IS NULL"))
                print("✓ Se asignó 'Macho' como valor por defecto para los animales existentes")
            
            return True
        except Exception as e:
            print(f"✗ Error al migrar: {str(e)}")
            return False

if __name__ == '__main__':
    print("Iniciando migración...")
    if migrate_add_genero():
        print("\n✓ Migración completada exitosamente")
        sys.exit(0)
    else:
        print("\n✗ Error en la migración")
        sys.exit(1)
