import sys
from .config import run
from gunicorn.app.wsgiapp import PORT
if __name__ == '__main__':
    sys.argv = "gunicorn --bind 0.0.0.0:5000 app:app".split()
    sys.exit(run())
