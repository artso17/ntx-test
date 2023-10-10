# Gunakan `python:3.11.4` sebagai base image
FROM python:3.11.4

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./api.py api.py

# Change the CMD to ENTRYPOINT because it is not expecting the overriding 
ENTRYPOINT ["python", "api.py"] 
