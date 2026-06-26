from pathlib import Path
p = Path(r'c:\Users\renzo\OneDrive\Documentos\python\proyecto 2\app.py')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()
start = None
for i, line in enumerate(lines):
    if line.strip() == 'for subfolder in sorted(os.listdir(categoria_path)):' and i > 1560:
        start = i - 1
        break
if start is None:
    raise SystemExit('start not found')
end = None
for i in range(start, len(lines)):
    if lines[i].strip() == 'db.session.commit()':
        # ensure this is the commit of this block by checking next non-empty is def seed_default_consejos
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j < len(lines) and lines[j].strip().startswith('def seed_default_consejos'):
            end = i
            break
if end is None:
    raise SystemExit('end not found')
new_block = [
'        orden = 0',
'',
'        def procesar_md_folder(source_path, title_hint=None):',
'            nonlocal orden',
'            md_files = [f for f in os.listdir(source_path) if f.lower().endswith(\'.md\')]',
'            if not md_files:',
'                return',
'',
'            relative_path = os.path.relpath(source_path, consejos_data_path).replace(\\'\\\\\\'\\, \\'/\\')',
'            for md_file in sorted(md_files):',
'                md_path = os.path.join(source_path, md_file)',
'                with open(md_path, \'r\', encoding=\'utf-8\') as f:',
'                    contenido_md = f.read()',
'',
'                titulo_match = re.search(r\'^#\\s+(.+?)$\', contenido_md, re.MULTILINE)',
'                titulo = titulo_match.group(1) if titulo_match else title_hint or os.path.splitext(md_file)[0].replace(\'_\', \' \\').title()',
'',
'                imagen = None',
'                img_files = [f for f in os.listdir(source_path) if f.lower().endswith((\'.jpg\', \' .jpeg\', \' .png\', \' .gif\'))]',
'                if img_files:',
'                    imagen = f\'uploads/consejos/{relative_path}/{img_files[0]}\'',
'',
'                contenido_limpio = re.sub(r\'^\\*\
$script = @'
from pathlib import Path
p = Path(r'c:\Users\renzo\OneDrive\Documentos\python\proyecto 2\app.py')
text = p.read_text(encoding='utf-8')
old = '''        orden = 0
        for subfolder in sorted(os.listdir(categoria_path)):
            subfolder_path = os.path.join(categoria_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            
            md_files = [f for f in os.listdir(subfolder_path) if f.endswith('.md')]
            if not md_files:
                continue
            
            md_file = md_files[0]
            md_path = os.path.join(subfolder_path, md_file)
            
            with open(md_path, 'r', encoding='utf-8') as f:
                contenido_md = f.read()
            
            titulo_match = re.search(r'^#\s+(.+?)$', contenido_md, re.MULTILINE)
            titulo = titulo_match.group(1) if titulo_match else subfolder.replace('_', ' ').title()
            
            imagen = None
            img_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            if img_files:
                imagen = f'uploads/consejos/{folder_name}/{subfolder}/{img_files[0]}'
            
            contenido_limpio = re.sub(r'^\*"[^\"]*\.(jpg|jpeg|png|gif)"\*\s*$', '', contenido_md, flags=re.MULTILINE | re.IGNORECASE)
            contenido_limpio = re.sub(r'^\*"?[A-Z]:\\[^\"]*\.(jpg|jpeg|png|gif)"?\*?\s*$', '', contenido_limpio, flags=re.MULTILINE | re.IGNORECASE)
            contenido_limpio = re.sub(r'!\[.*?\]\([^)]*\.(jpg|jpeg|png|gif)\)', '', contenido_limpio, flags=re.IGNORECASE)
            
            contenido_html = markdown.markdown(contenido_limpio)
            
            sub = SubConsejoMarkdown(
                consejo_id=consejo.id,
                titulo=titulo,
                contenido=contenido_html,
                imagen=imagen,
                orden=orden
            )
            db.session.add(sub)
            orden += 1
        
        db.session.commit()
'''
new = '''        orden = 0

        def procesar_md_folder(source_path, title_hint=None):
            nonlocal orden
            md_files = [f for f in os.listdir(source_path) if f.lower().endswith('.md')]
            if not md_files:
                return

            relative_path = os.path.relpath(source_path, consejos_data_path).replace('\\', '/')
            for md_file in sorted(md_files):
                md_path = os.path.join(source_path, md_file)
                with open(md_path, 'r', encoding='utf-8') as f:
                    contenido_md = f.read()

                titulo_match = re.search(r'^#\s+(.+?)$', contenido_md, re.MULTILINE)
                titulo = titulo_match.group(1) if titulo_match else title_hint or os.path.splitext(md_file)[0].replace('_', ' ').title()

                imagen = None
                img_files = [f for f in os.listdir(source_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                if img_files:
                    imagen = f'uploads/consejos/{relative_path}/{img_files[0]}'

                contenido_limpio = re.sub(r'^\*"[^\"]*\.(jpg|jpeg|png|gif)"\*\s*$', '', contenido_md, flags=re.MULTILINE | re.IGNORECASE)
                contenido_limpio = re.sub(r'^\*"?[A-Z]:\\[^\"]*\.(jpg|jpeg|png|gif)"?\*?\s*$', '', contenido_limpio, flags=re.MULTILINE | re.IGNORECASE)
                contenido_limpio = re.sub(r'!\[.*?\]\([^)]*\.(jpg|jpeg|png|gif)\)', '', contenido_limpio, flags=re.IGNORECASE)

                contenido_html = markdown.markdown(contenido_limpio)

                sub = SubConsejoMarkdown(
                    consejo_id=consejo.id,
                    titulo=titulo,
                    contenido=contenido_html,
                    imagen=imagen,
                    orden=orden
                )
                db.session.add(sub)
                orden += 1

        procesar_md_folder(categoria_path, title_hint=categoria_nombre)

        for subfolder in sorted(os.listdir(categoria_path)):
            subfolder_path = os.path.join(categoria_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue

            procesar_md_folder(subfolder_path, title_hint=subfolder.replace('_', ' ').title())

        db.session.commit()
'''
if old not in text:
    raise SystemExit('old not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print('patched')
