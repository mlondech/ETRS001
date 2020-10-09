FROM python:3
RUN apt-get update
RUN apt-get -y install libpython3-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt