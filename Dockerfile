FROM nodejs as nodejsbuilder
FROM gcc:8.2.0-centos7 as gccbuilder
FROM python:3.7-centos7

COPY --from=gccbuilder /usr/local/gcc-8.2.0 /usr/local/gcc-8.2.0

ENV LD_LIBRARY_PATH=/usr/local/gcc-8.2.0/lib64:${LD_LIBRARY_PATH}

RUN yum install -y \
	    gmp-devel \
	    mpfr-devel \
	    libmpc-devel

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ \
        --no-cache-dir \
        -r requirements.txt

COPY paddlewebocr paddlewebocr

RUN python paddlewebocr/pkg/ocr.py

COPY --from=nodejsbuilder /app/dist webui/dist

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8080

VOLUME /app/logs

CMD ["uvicorn", "paddlewebocr.main:app", "--host", "0.0.0.0", "--port", "8080"]
