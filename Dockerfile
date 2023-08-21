FROM python:3.9
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]