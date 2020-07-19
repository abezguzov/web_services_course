FROM python:3.6-slim
WORKDIR /root
RUN pip install flask gunicorn numpy sklearn scipy joblib flask_wtf pandas
COPY . /root