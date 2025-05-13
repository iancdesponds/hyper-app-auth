FROM python:3.12-slim
WORKDIR /auth
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x ./uvicorn.sh
ENV PYTHONPATH=/auth/app
CMD ["./uvicorn.sh"]
