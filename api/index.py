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


def handler(request, response):
    if awsgi is None:
        raise RuntimeError('awsgi is required for Vercel deployment. Install it with pip on Linux or use the Vercel environment.')
    return awsgi.response(app, request.environ, response)
