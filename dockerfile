#syntax=docker/dockerfile:1
FROM tensorflow/tensorflow
# FROM python:latest
WORKDIR /app
COPY require.txt .
RUN pip install -r require.txt
COPY . .
RUN python create_model.py
CMD [ "python3", "app.py"]
