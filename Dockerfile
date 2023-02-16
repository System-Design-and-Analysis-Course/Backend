FROM python:3.10.2-bullseye

USER root

RUN apt-get update -qq && apt-get install -qqy gettext

WORKDIR /src/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN django-admin compilemessages

RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]



