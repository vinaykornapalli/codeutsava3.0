FROM ubuntu:18.04

COPY . /app

RUN apt-get update 
RUN apt-get install -y apt-utils 
RUN apt-get install -y python3-pip 
RUN apt-get install -y tesseract-ocr 
RUN apt-get install -y libleptonica-dev 
RUN apt-get install -y libtesseract-dev 
RUN pip3 install virtualenv
RUN virtualenv venv
RUN /bin/bash -c "source /venv/bin/activate"
RUN pip3 install -r /app/requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN pip3 install flask
ENTRYPOINT ["python3"]
CMD ["/app/app.py"]
