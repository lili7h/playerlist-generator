FROM python:3.11.7-slim-bullseye

WORKDIR /playerlist-API

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD [ "python3", "-m" , "flask", "--app=api.py", "run", "--host=0.0.0.0", "--port=8080"]