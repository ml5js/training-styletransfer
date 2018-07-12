FROM tensorflow/tensorflow:1.4.1-gpu

LABEL maintainer="Cris Valenzuela <cv965@nyu.edu>"

RUN apt-get update
RUN apt-get install wget -y
RUN apt-get update && apt-get install -y software-properties-common

# Install "ffmpeg"
RUN add-apt-repository ppa:mc3man/xerus-media
RUN apt-get update && apt-get install -y ffmpeg

# Copy all files in directory
COPY . /styletransfer
# COPY requirements.txt /styletransfer

WORKDIR "/styletransfer"

# Install dependencies
RUN pip install -r requirements.txt

RUN mkdir /styletransfer/data
WORKDIR "/styletransfer/data"
RUN wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
RUN wget http://images.cocodataset.org/zips/train2014.zip
RUN unzip train2014.zip

WORKDIR "/styletransfer"