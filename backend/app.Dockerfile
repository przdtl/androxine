FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./manage.py .
COPY ./androxine ./androxine

RUN mkdir staticfiles

COPY ./script.sh ./
RUN chmod +x /app/script.sh

ENTRYPOINT ["sh", "./script.sh"]