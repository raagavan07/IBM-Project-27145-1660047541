FROM python:3.10.4
LABEL maintainer="Raagavan, raagavan@student.tce.edu"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install ibm_db
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]