FROM resin/rpi-raspbian:wheezy-2015-01-15

RUN apt-get install -y wget

RUN wget -O - http://www.codeminders.com/raspbian-apt/KEY.txt | apt-key add -

RUN echo "\ndeb http://www.codeminders.com/raspbian-apt/ wheezy main" >> /etc/apt/sources.list

# Install Python.
RUN apt-get update
RUN apt-get install -y python python-dev python-pip python-pygame libraspberrypi-bin

# Install libopencv
RUN apt-get install -y libopencv-dev

RUN apt-get install -y nano libraspberrypi-bin fbi

RUN apt-get install -y python-opencv


ADD . /app

RUN pip install pygame
RUN pip install picamera

EXPOSE 8080

RUN echo "udevd --daemon" > /start
RUN echo  "modprobe spi-bcm2708" >> /start
RUN echo  "modprobe fbtft_device name=pitft verbose=0 rotate=270" >> /start
RUN echo python app/hello.py >> /start
RUN chmod +x /start

