FROM python:latest

WORKDIR /usr/share/app
# Copy app files from local to container
COPY application ./
COPY web_app_debug.py ./

#RUN pip install flask
# Install app requirements via pip
RUN pip install -r requirements.txt

CMD ["./app.py"]
#CMD ["python",""]
#CMD ["top"]
#CMD ["python","web_app_debug.py"]

