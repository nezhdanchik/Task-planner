FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
COPY ./frontend ./frontend
ENTRYPOINT ["uvicorn", "app.api.endpoints.main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
