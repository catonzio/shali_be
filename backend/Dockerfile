# FROM nginx:1.21.1-alpine
# COPY nginx.conf /etc/nginx/conf.d/default.conf

FROM python:latest
 
WORKDIR /shali

COPY ./requirements.txt /shali/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /shali/requirements.txt

COPY ./src /shali/src

WORKDIR /shali/src

CMD ["python3", "main.py"]

