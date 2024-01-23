FROM python:latest
WORKDIR /app
RUN pip install tk
RUN pip install matplotlib 
ENTRYPOINT export DISPLAY=172.25.240.1:0
COPY . /app
CMD ["python3", "p.py"]
CMD ["python", "molecula.py"]
