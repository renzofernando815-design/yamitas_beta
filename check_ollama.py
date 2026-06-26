import os
import shutil
import subprocess

DEFAULT_OLLAMA_COMMAND = (
    r'C:\Users\renzo\AppData\Local\Programs\Ollama\ollama.exe' if os.name == 'nt' else 'ollama'
)


def get_ollama_command():
    command = os.environ.get('OLLAMA_COMMAND') or DEFAULT_OLLAMA_COMMAND
    if os.path.isabs(command):
        if os.path.exists(command):
            return command
        found = shutil.which(command)
        return found
    return shutil.which(command)


def parse_ollama_list_output(output):
    lines = output.strip().splitlines()
    if len(lines) <= 1:
        return []
    models = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.strip().split()
        if parts:
            models.append(parts[0])
    return models


def main():
    ollama_command = get_ollama_command()
    if not ollama_command:
        print('Ollama no está instalado o no se encuentra el ejecutable.')
        print('Instala Ollama y define OLLAMA_COMMAND si es necesario.')
        return

    print(f'Ollama encontrado en: {ollama_command}')
    try:
        result = subprocess.run(
            [ollama_command, 'list'],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print('No se pudo obtener la lista de modelos.')
            print(result.stderr.strip())
            return

        installed = parse_ollama_list_output(result.stdout)
        if not installed:
            print('No hay modelos instalados en Ollama.')
        else:
            print('Modelos instalados:')
            for model in installed:
                print(f' - {model}')
            print('\nPuedes instalar un modelo con:')
            print('    ollama pull mistral')
    except FileNotFoundError:
        print('El ejecutable de Ollama no se pudo ejecutar.')


if __name__ == '__main__':
    main()
