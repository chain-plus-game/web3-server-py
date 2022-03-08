FROM tiangolo/uvicorn-gunicorn-fastapi


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

