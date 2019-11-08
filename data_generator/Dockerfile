FROM python:latest

WORKDIR /usr/share/app

# Copy app files from local to container
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY application ./
CMD ["python","docker_debugger.py"]



