from app import app

# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04
# https://stackoverflow.com/questions/46259678/understanding-gunicorn-and-flask-on-docker-docker-compose
if __name__ == "__main__":
    app.run()
