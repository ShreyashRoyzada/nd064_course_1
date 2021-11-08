FROM python:2.7
LABEL maintainer = "ShreyashRoyzada"

WORKDIR /app

COPY . /app
RUM pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python init_db.py

EXPOSE 3111

CMD ["python","app.py"]
