FROM python:3.8

RUN mkdir -p /usr/scr/app/
WORKDIR /usr/scr/app/

COPY . /usr/scr/app/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","app.py"]

