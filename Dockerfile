FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --update wkhtmltopdf
RUN apk --no-cache update \
    && apk --no-cache upgrade \
    && apk add --no-cache \
            mysql-client \
            freetype \
            libpng \
            freetype-dev \
            libpng-dev \
            jpeg-dev \
            libjpeg \
            libjpeg-turbo-dev \
            wget \
            zlib-dev \
            ttf-freefont \
            fontconfig \
            xvfb \
            libxrender-dev \
            gettext \
            gettext-dev \
            libxml2-dev \
            gnu-libiconv-dev \
            autoconf \
            g++ \
            git \
            bash \
            wkhtmltopdf
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 3306
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
