FROM python:3.12

WORKDIR /conector_meet

COPY connector.py /conector_meet
COPY requirements.txt /conector_meet

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

RUN pip install --trusted-host pypi.python.org --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "connector:app", "--host", "0.0.0.0", "--port", "80"]
