FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean
WORKDIR /app
COPY  . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
