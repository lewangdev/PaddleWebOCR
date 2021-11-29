sudo docker build . -f Dockerfile-gcc-8.2.0-centos7 -t gcc:8.2.0-centos7
sudo docker build . -f Dockerfile-nodejs -t nodejs
sudo docker build . -f Dockerfile-python-3.7-centos7 -t python:3.7-centos7
sudo docker build . -t paddlewebocr
