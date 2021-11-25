FROM paddlepaddle:2.2.0-centos7

WORKDIR /usr/src

COPY requirements.txt requirements.txt

RUN yum install -y gcc-c++ mesa-libGL && pip install -i https://mirror.baidu.com/pypi/simple/  \
        --no-cache-dir \
	-r requirements.txt

ENV LD_LIBRARY_PATH=/usr/local/gcc-8.2.0/lib64:${LD_LIBRARY_PATH}

COPY paddlewebocr paddlewebocr

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080

CMD ["python", "paddlewebocr/main.py"]
