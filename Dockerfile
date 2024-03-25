FROM python:3.9.19-alpine3.19

RUN apk add --no-cache py3-pip && \
    pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD [ "-h" ]
