FROM python:3.12
EXPOSE 5000
WORKDIR /
RUN pip install flask flask-restful
RUN pip3 install flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]