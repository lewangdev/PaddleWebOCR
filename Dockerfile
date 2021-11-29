FROM nodejs as nodejsbuilder
FROM paddlepaddle:2.2.0-centos7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN yum install -y gcc-c++ mesa-libGL && pip install -i https://mirror.baidu.com/pypi/simple/  \
        --no-cache-dir \
        -r requirements.txt

ENV LD_LIBRARY_PATH=/usr/local/gcc-8.2.0/lib64:${LD_LIBRARY_PATH}

COPY paddlewebocr paddlewebocr

COPY --from=nodejsbuilder /app/dist paddlewebocr/dist

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080

VOLUME /app/logs

CMD ["python", "paddlewebocr/main.py"]
