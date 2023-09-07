FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -U

COPY . /app

# CMD ["python3", "-m", "checkuser"]
ENTRYPOINT [ "python3", "-m", "checkuser" ]