# PaddleWebOCR

开源的中英文离线 OCR，使用 PaddleOCR 实现，提供了简单的 Web 页面及接口。

An opensource offline multi-languages OCR system shipped with RESTful api and web page.

## 介绍

**使用了开源的 PaddleOCR 并内置了多个模型，可以在离线环境下运行，并且相关资料丰富便于自行训练模型。PaddleOCR 本身支持中文简体繁体，英文，韩文等等多种语言，本项目只内置了中英文（简体中文和繁体中文）的模型，如需要识别其它语言，可以参考本项目调整模型。**


![web页面](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/webui.png?raw=true)  


## 特性

* paddle 2.2.0
* paddleocr 2.3.0.2
* 中英文识别，可选用不同的模型快速识别
* 文字检测
* 中文简体/繁体，英语等多语种识别

## 安装需求  
 
### 运行平台  

* ✔ Python 3.7+  
* ✔ CentOS 7   
* ✔ MacOS Big Sur 
* ✔ Docker   

CentOS 和 MacOS 系统下可以直接部署使用，目前只构建了 paddlepaddle 的 CPU 版本，不支持 GPU。也过通过构建 Docker 镜像或者直接从 DockerHub 拉去镜像来使用。

### 最低配置要求  

* CPU:    2 核  
* 内存:    4GB  

## 安装说明  

### 服务器部署

1. 安装python3.7  
    
2. 安装依赖包  

``` shell script
pip install -r requirements.txt
```  

3. 运行，项目默认运行在 8080 端口：  

``` shell script
python paddlewebocr/main.py [--port=8080]
```

### Docker 部署  


推荐从 DockerHub pull 运行镜像

```shell script
docker run -d -p 8080:8080 -v ${PWD}/logs:/app/logs --name paddlewebocr lewangdev/paddlewebocr:latest
```  

使用脚本构建本地镜像（因为要编译 GCC，整个构建过程非常漫长）

```shell script
# Dockerfile 构建
./build-docker-image.sh

# 运行镜像
docker run -d -p 8080:8080 -v ${PWD}/logs:/app/logs --name paddlewebocr paddlewebocr:latest 
```  
  

## 接口调用示例  

* Python 使用 File 上传文件  

``` python
import requests
url = 'http://192.168.52.65:8080/api/ocr'
img1_file = {
    'file': open('img1.png', 'rb')
}
res = requests.post(url=url, data={'compress': 0}, files=img1_file)
```  

* Python 使用 Base64  

``` python
import requests
import base64
def img_to_base64(img_path):
    with open(img_path, 'rb')as read:
        b64 = base64.b64encode(read.read())
    return b64
    
url = 'http://192.168.52.65:8080/api/ocr'
img_b64 = img_to_base64('./img1.png')
res = requests.post(url=url, data={'img': img_b64})
```

## 效果展示  

![英文文档识别](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/doc-1.png?raw=true)  

![中文文档识别](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/doc-2.png?raw=true)  

![验证码识别](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/verifycode-1.png?raw=true)

![验证码识别](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/verifycode-2.png?raw=true)

![火车票](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/train-ticket-1.png?raw=true)

![火车票](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/train-ticket-2.png?raw=true)

![发票](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/fapiao-1.png?raw=true)

![身份证](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/idcard-1.png?raw=true)

![海报](https://github.com/lewangdev/PaddleWebOCR/blob/master/images/haibao-1.png?raw=true)

## 更新记录  

* 2021年11月26日  
    发布 1.0.0 版本，仅支持 CPU


## 致谢

本项目参考了 [TrWebOCR](https://github.com/alisen39/TrWebOCR)，由于 TrWebOCR 启动时需要联网并且它使用的 [Tr](https://github.com/myhub/tr) 相关的资料比较少，故而尝试使用 [paddlepaddle](https://github.com/PaddlePaddle/Paddle) 和 [paddleocr](https://github.com/PaddlePaddle/PaddleOCR) 来替换 Tr， 从而有了本项目。


## License  

Apache 2.0
