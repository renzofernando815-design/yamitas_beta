import os
import mimetypes
try:
    import awsgi
except ImportError:
    awsgi = None

from app import app, db, sync_global_sources_from_json

with app.app_context():
    try:
        db.create_all()
    except Exception:
        pass

    try:
        sync_global_sources_from_json()
    except Exception:
        pass


def serve_static_file(path):
    """Serve static files directly without going through Flask."""
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    file_path = os.path.join(static_folder, path)
    
    # Security: prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(static_folder)):
        return None
    
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': mime_type,
                'Cache-Control': 'public, max-age=31536000, immutable'
            },
            'body': content.decode('utf-8') if mime_type.startswith('text/') else content,
            'isBase64Encoded': not mime_type.startswith('text/')
        }
    
    return None


def handler(request, response):
    # Handle static file requests
    path = request.environ.get('PATH_INFO', '').lstrip('/')
    if path.startswith('static/'):
        static_response = serve_static_file(path[7:])  # Remove 'static/' prefix
        if static_response:
            response(
                f"{static_response['statusCode']} OK",
                [(k, v) for k, v in static_response['headers'].items()]
            )
            content = static_response['body']
            if isinstance(content, str):
                return [content.encode('utf-8')]
            return [content]
    
    if awsgi is None:
        raise RuntimeError('awsgi is required for Vercel deployment. Install it with pip on Linux or use the Vercel environment.')
    return awsgi.response(app, request.environ, response)
