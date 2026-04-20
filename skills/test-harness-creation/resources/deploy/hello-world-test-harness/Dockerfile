FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi "uvicorn[standard]"

COPY server_example.py /app/server_example.py
COPY health_container_check.py /app/health_container_check.py

EXPOSE 8000

CMD ["uvicorn", "server_example:app", "--host", "0.0.0.0", "--port", "8000"]
