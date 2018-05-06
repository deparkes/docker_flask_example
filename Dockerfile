FROM python:3.4-alpine
COPY . /web
WORKDIR /web/api
RUN pip install -r ./requirements.txt
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]