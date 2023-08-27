FROM python:3.9
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN pip install -r requirements.txt
ENV FLASK_APP=main.py
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0"]