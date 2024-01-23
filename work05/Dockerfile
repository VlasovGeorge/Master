FROM python:latest
WORKDIR ./app
RUN pip install tk
RUN pip install matplotlib 
RUN export DISPLAY=:1
COPY . /app
CMD ["echo", "Hello, World!"]
