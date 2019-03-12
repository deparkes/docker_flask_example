An example of a flask api running in a docker container.

Extends example of a Flask API from [programminghistorian.org](http://programminghistorian.github.io/ph-submissions/lessons/creating-apis-with-python-and-flask)

# Requirements
[docker](https://www.docker.com/get-docker)

# Usage
Clone this repository
```
git clone https://github.com/deparkes/docker_flask_example.git
```

Run docker-compose
```
docker-compose up --build
```

Test localhost api in your browser by navigating to
```
http://localhost:5000/api/v1/resources/books/all
```

# Notes

## nginx
https://dev.to/domysee/setting-up-a-reverse-proxy-with-nginx-and-docker-compose-29jg

https://blog.docker.com/2015/04/tips-for-deploying-nginx-official-image-with-docker/
