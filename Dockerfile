FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "172.29.0.2", "--port", "8001"]


