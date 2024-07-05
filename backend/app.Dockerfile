FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONPATH=/app/androxine

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./androxine ./androxine

RUN mkdir -p ./androxine/staticfiles

COPY ./script.sh ./
RUN chmod +x /app/script.sh

ENTRYPOINT ["sh", "./script.sh"]