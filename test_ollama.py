from app import call_ollama, app

print('OLLAMA_COMMAND=', getattr(__import__('app'), 'OLLAMA_COMMAND', None))
print('OLLAMA_MODEL=', getattr(__import__('app'), 'OLLAMA_MODEL', None))

response, error = call_ollama('Hola, ¿cómo estás?')
print('response=', repr(response))
print('error=', repr(error))

with app.test_client() as client:
    r = client.post('/api/chat', json={'message': 'Hola prueba'})
    print('status=', r.status_code)
    print('data=', r.get_data(as_text=True))
    try:
        print('json=', r.get_json())
    except Exception as e:
        print('json exception=', e)
