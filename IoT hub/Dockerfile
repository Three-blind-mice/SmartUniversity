FROM python:3.8
#ADD exception.py /IoT-hub/
#ADD iotdriver.py /IoT-hub/
#ADD settings.py /IoT-hub/
#ADD message_handler.py  /IoT-hub/
ADD main.py /IoT-hub/
#ADD lmsdriver.py /IoT-hub/
ADD driver.exe /IoT-hub/
#ADD imgs /IoT-hub/

RUN pip install --upgrade pip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip install selenium==3.8.0
WORKDIR /IoT-hub/
CMD ["python", "main.py"]