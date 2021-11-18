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
flask run
```