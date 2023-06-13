## Compose sample application

### Use with Docker Development Environments

You can open this sample in the Dev Environments feature of Docker Desktop version 4.12 or later.


### Python/Flask application with Nginx proxy and a Mongo database

```

[_compose.yaml_](compose.yaml)
```
services:
  web:
    build: app
    ports:
    - 80:80
  backend:
    build: flask_app
    ...
  mongo:
    image: mongo
```
The compose file defines an application with three services `web`, `backend` and `db`.
When deploying the application, docker compose maps port 80 of the web service container to port 80 of the host as specified in the file.
Make sure port 80 on the host is not being used by another container, otherwise the port should be changed.

## Deploy with docker compose

```
$ docker compose up -d
Creating network "nginx-flask-mongo_default" with the default driver
Pulling mongo (mongo:)...
latest: Pulling from library/mongo
423ae2b273f4: Pull complete
...
...
Status: Downloaded newer image for nginx:latest
Creating nginx-flask-mongo_mongo_1 ... done
Creating nginx-flask-mongo_backend_1 ... done
Creating nginx-flask-mongo_web_1     ... done

```

## Expected result

Listing containers must show three containers running and the port mapping as below:
```
$ docker ps
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                  NAMES
a0f4ebe686ff        nginx                       "/bin/bash -c 'envsu…"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp     nginx-flask-mongo_web_1
dba87a080821        nginx-flask-mongo_backend   "./server.py"            About a minute ago   Up About a minute                          nginx-flask-mongo_backend_1
d7eea5481c77        mongo                       "docker-entrypoint.s…"   About a minute ago   Up About a minute   27017/tcp              nginx-flask-mongo_mongo_1
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:
```
$ curl localhost:80
Hello from the Docker demo!
```

Stop and remove the containers
```
$ docker compose down


```
add aws access key and secret key in aws_creds.py file
Upload a csv file using the url http://localhost:80/v1/upload with file kwy file