FROM nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04

ENV APP_DIR=/app
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR/

RUN apt update && apt upgrade -y && \
    apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt install python3.9 -y && apt install python3-pip -y && \
    apt install python3.9-dev -y

RUN apt-get install -y libsm6 libxrender1 libfontconfig1 libxext6 libgl1-mesa-glx && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -U --no-cache-dir -r $APP_DIR/requirements.txt

ENTRYPOINT [ "bash" ]