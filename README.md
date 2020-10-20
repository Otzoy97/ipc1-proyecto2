# Flask api

Ejemplo de api en python-flask para desplegar en heroku

## Ejecutar localmente
Tener instalado localmente:
 - mongodb v4.4 o superior
 - python 3.6.9 o superior

```sh
$ pip3 install --user pipenv

$ git clone https://github.com/Otzoy97/ipc1-proyecto2.git
$ cd ipc1-proyecto2

$ pipenv install

$ pipenv shell

$ python app.py
```

La aplicación debería estar corriendo en [localhost:5000](http://localhost:5000/)

## Desplegar en heroku
Tener instalado [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) y configurar la cuenta a utilizar para desplegar la aplicación.
Poseer un cluster en [mongoDB Atlas](https://docs.atlas.mongodb.com/getting-started/).


```sh
$ heroku create
$ git push heroku main

$ heroku config:set MONGO_URI=<mongo_uri>

$ heroku config:set JWT_SECRET_KEY=<secret_key>
```
Reemplazar <mongo_uri> con la [cadena de conección](https://docs.atlas.mongodb.com/connect-to-cluster/#use-the-connect-dialog-to-connect-to-your-cluster) del cluster de mongoDB Atlas y <secret_key> con un texto que sea difícil de adivinar.

----

Para consumir los servicios utilizar la <i>Web URL</i> que provee heroku para la aplicación recién desplegada. 

```ssh
$ heroku info
```

## Referencias
[Flask Rest API - Zero to Yoda](https://dev.to/paurakhsharma/series/3672)<br>
[Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)

## LICENSE
[GNU General Public License v3.0](https://github.com/Otzoy97/ipc1-proyecto2/blob/main/LICENSE)