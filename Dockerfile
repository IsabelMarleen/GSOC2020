FROM amancevice/pandas:0.24.2-alpine

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

COPY . .

EXPOSE 5000

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py

CMD ["waitress-serve", "--port=5000", "app:app" ]
