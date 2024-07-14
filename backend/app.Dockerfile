FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONPATH=/app/androxine

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./androxine ./androxine

RUN mkdir -p ./androxine/staticfiles

COPY ./entrypoint.sh ./
COPY ./scripts ./scripts

RUN chmod +x ./entrypoint.sh -R ./scripts 

ENTRYPOINT ["sh", "./entrypoint.sh"]