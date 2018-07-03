FROM tensorflow/tensorflow:0.11.0-gpu

LABEL maintainer="Cris Valenzuela <cv965@nyu.edu>"

RUN apt-get update
RUN apt-get install wget -y

# Copy all files in directory
COPY . /styletransfer

WORKDIR "/styletransfer"

# Install dependencies
RUN pip install -r requirements.txt

# Copy all files in directory
# WORKDIR "/styletransfer/data"
# RUN wget http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
# RUN wget http://images.cocodataset.org/zips/train2014.zip
# RUN unzip train2014.zip
