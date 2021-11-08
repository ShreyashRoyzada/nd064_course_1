FROM python:2.7
LABEL maintainer = "ShreyashRoyzada"

WORKDIR /app

COPY . /app
RUN pip install --upgrade pip

RUN pip install -r ./project/techtrends/requirements.txt

RUN python init_db.py

EXPOSE 3111

CMD ["python","app.py"]
