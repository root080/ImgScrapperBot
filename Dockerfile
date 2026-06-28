FROM python:3

ADD .env .
ADD imgscrapperbot.py .
ADD requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "imgscrapperbot.py"]
