FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /tmp
WORKDIR /tmp
RUN pip3 install --default-timeout=20 --no-cache-dir -r requirements.txt
ENV PORT 8080
CMD ["flask", "run", "--host", "0.0.0.0", "-p", "8080"]