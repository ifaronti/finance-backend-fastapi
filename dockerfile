FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY venv ./venv
COPY main.py .
COPY placeholders.json .
COPY .env .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]