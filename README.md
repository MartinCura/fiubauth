**FIUBAuth**
============

Prototipo de un sistema de autenticación y autorización basado en OpenID Connect, para ser usado en la Facultad de Ingeniería de la Universidad de Buenos Aires.

[Informe de este proyecto](https://drive.google.com/open?id=10I6nxXT1qVovWpPzGUywH0uXMXhq8BuR)


## Set-up

Se recomienda trabajar en un ambiente virtual (aqui se utiliza [venv](https://docs.python.org/3/library/venv.html)):
```bash
$ python3 -m venv fiubauth_venv
$ source fiubauth_venv/bin/activate
```

Para instalar las librerias necesarias:
```bash
$ pip install -r requirements.txt
```

Para crear la base de datos y darle privilegios a *fiubauth*:
```bash
$ sudo su - postgres
postgres~$ psql
```
```sql
CREATE DATABASE fiubauth_db;
CREATE USER fiubauth WITH PASSWORD 'fiupass';
ALTER ROLE fiubauth SET client_encoding TO 'utf8';
ALTER ROLE fiubauth SET default_transaction_isolation TO 'read committed';
ALTER ROLE fiubauth SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fiubauth_db TO fiubauth;
```

Ahora se pueden llevar a cabo las migraciones, generar una clave RSA y crear un superusuario:

```bash
$ python manage.py migrate
$ python manage.py creatersakey
$ python manage.py createsuperuser
```


## Uso

Para crear usuarios por el momento se debe hacer programáticamente.
```bash
$ python manage.py shell
```
```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('mahatmagandhi', 'mahatmagandhi@protonmail.com', 'humanityisanocean')
```
Este `user` puede ser modificado directamente, mientras después se utilice `.save()` para guardar los cambios.

En cualquier momento se puede correr el servidor mediante:
```bash
$ python manage.py runserver [puerto, predeterminado: 8000]
```
y encontrarlo en http://localhost:8000.

Endpoints principales:
* `/admin` (administración)
* `/accounts/login` y `/accounts/logout` (inicio y cierre de sesión)
* `/` o `/home` (lista los clientes a los cuales el usuario actual dio permisos)
* `/auth` (endpoints que utiliza OIDC)


### Registrar clientes (*relying parties*)

Los clientes son aquellos sitios o servicios que quieran utilizar **FIUBAuth** para autenticar a sus usuarios. Se los puede registrar mediante la consola de administración.

Dirigirse a `/admin`, iniciar sesión como el superusuario creado y dirigirse a la sección Clients para agregar uno nuevo. Ponerle un nombre identificatorio, los *response types* que se desee (ejemplo: `code`, `id_token token`), y como *redirect_uri* aquella del servicio. Para más información ver el ejemplo más abajo o la [documentación de la librería OIDC](https://django-oidc-provider.readthedocs.io/en/latest/sections/relyingparties.html).


## Ejemplo de Relying Party

En la carpeta `example-rp` acompaña al proyecto un ejemplo mínimo de un servicio que puede usar *FIUBAuth* para identificar al usuario y obtener información suya. Nota: este ejemplo hace uso de una [librería de funciones de OIDC](https://www.sakimura.org/test/openidconnect.js); ver las licencias correspondientes.

Primero debe crearse un cliente (ver más arriba) con por lo menos `id_token token` como *response_type* y redirect_uri apropiada: 'http://localhost:3003'. Al guardarlo tomar nota del *CLIENT ID*.

Hecho esto, se puede servir la página (asume que *fiubauth* se encuentra en el puerto 8000 local) mediante:
```bash
$ python -m http.server 3003
```

Dirigirse a http://localhost:3003, setear el *client id*, guardar, y vea que pasa al iniciar sesión.

[Demostración](https://drive.google.com/open?id=1RJxHTqoiFLtGqoOVeUvuIBzjhchCyz5-)
