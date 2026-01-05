FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r core_service/requirements.txt

CMD ["uvicorn", "core_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
