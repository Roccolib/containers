#image de base
from ubuntu:kub
#maintainer of the image
LABEL maintainer="Richard"
# Update the image to the latest packages
RUN apt-get update
#add pip repository
RUN echo deb deb http://fr.archive.ubuntu.com/ubuntu/ bionic universe multiverse; apt-get update
#add pip to install dependencies
RUN apt-get install python3-pip -y  # && apt-get install curl -y
#add libraries for python api
RUN pip3 install flask && pip3 install requests && pip3 install kafka-python
#expose port 5000
expose 5000
