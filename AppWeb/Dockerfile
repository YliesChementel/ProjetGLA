FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean
WORKDIR /app
COPY  . /app
RUN pip install --no-cache-dir -r ./requirements.txt
ENV DB_PATH /shared/instance/Crypto.db
EXPOSE 5000
CMD ["python3", "run.py"]
