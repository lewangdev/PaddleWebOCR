docker build . -f Dockerfile-gcc-8.2.0-centos7 -t gcc:8.2.0-centos7
docker build . -f Dockerfile-python-3.7-centos -t python:3.7-centos7
docker build . -f Dockerfile-paddlepaddle-2.2.0-centos7 -t paddlepaddle:2.2.0-centos7
docker build . -t paddlewebocr
