# My Personal Blog Software

In this repo you can find the software with which I run my blog.
Currently, it's all still totally unfinished.... :D

## Development
Create virtual environment
```shell
python -m venv venv
source venv/bin/activate
```

Install requirements
```shell
pip install -r requirements.txt
```

To start the dev server 
```shell
export FLASK_APP=managed.py
export FLASK_ENV=development
export FLASK_DEBUG=1
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
flask run
```

To start the worker
```shell
celery -A worker.celery worker --loglevel=info
```

Yes, I know that celery is a bit much. ^^
But I would have had to implement something like cron jobs anyway, then I might as well do it that way. 