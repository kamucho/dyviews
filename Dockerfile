FROM python:3.8   
ENV PYTHONUNBUFFERED 1
RUN mkdir /dynamic_views
WORKDIR /dynamic_views
ADD . /dynamic_views/
RUN pip install -r requirements.txt
