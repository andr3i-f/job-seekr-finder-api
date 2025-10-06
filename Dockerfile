FROM python:3.13-slim

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["/bin/bash"]