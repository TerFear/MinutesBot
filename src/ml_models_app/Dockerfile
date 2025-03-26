FROM python:3.12

WORKDIR /app

COPY mailmodules.py /app
COPY ../conference_app/requirements.txt /app


RUN pip install  --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "mailmodules:app", "--host", "0.0.0.0", "--port", "8000"]
