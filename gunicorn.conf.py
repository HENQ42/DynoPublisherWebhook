import os
bind = "0.0.0.0:"+str(os.environ.get('PORT', 5000))
workers = 2
#gunicorn -c ./gunicorn.conf.py  wsgi:app