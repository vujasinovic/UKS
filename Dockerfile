FROM python:3.6-slim
MAINTAINER Mark Gituma <mark.gituma@gmail.com>

ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# CMD python manage.py runserver 0.0.0.0:8000
CMD python manage.py runserver --settings uks.settings_mini_kube 0.0.0.0:8000
# zeza
# RUN chmod +x start.sh 

