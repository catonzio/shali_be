FROM python:latest
 
WORKDIR /shali

COPY ./requirements.txt /shali/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /shali/requirements.txt

COPY ./src /shali/src

WORKDIR /shali/src

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python3", "main.py"]
