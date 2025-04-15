FROM python:3.9.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3-venv && \
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ["*.py", "./"]

EXPOSE 9696

ENTRYPOINT ["/bin/bash", "-c", "source venv/bin/activate && exec uvicorn app:app --host 0.0.0.0 --port 9696"]