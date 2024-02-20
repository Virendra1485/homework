FROM python:3.8
RUN mkdir homework
COPY . /homework
WORKDIR /homework
RUN pip install -r requirements.txt