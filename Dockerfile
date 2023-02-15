FROM python:3.10.2-bullseye

USER root

RUN apt-get update -qq && apt-get install -qqy gettext

WORKDIR /src/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#RUN ["chmod", "+x", "docker-entrypoint.sh"]
#ENTRYPOINT ["/src/docker-entrypoint.sh"]
#ENTRYPOINT ["./manage.py", "runserver", "8000"]



