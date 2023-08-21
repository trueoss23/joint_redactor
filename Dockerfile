FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY . .

RUN chmod +x wait-for-it.sh
RUN pip install --no-cache-dir -r requirements.txt
