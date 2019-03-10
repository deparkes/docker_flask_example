FROM python:3.4-alpine
COPY . /web
WORKDIR /web/api
RUN pip install -r ./requirements.txt
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["gunicorn", "wsgi:app"]
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8000"]
