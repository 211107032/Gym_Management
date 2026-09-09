import os
import shutil
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

if os.getenv('VERCEL') == '1' or 'VERCEL' in os.environ:
    base_dir = Path(__file__).resolve().parent.parent
    source_db = base_dir / 'db.sqlite3'
    tmp_db = Path('/tmp/db.sqlite3')
    if source_db.exists() and not tmp_db.exists():
        try:
            shutil.copy2(source_db, tmp_db)
        except Exception:
            pass

application = get_wsgi_application()

app = application
