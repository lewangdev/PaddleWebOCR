import requests
import base64


def img_to_base64(img_path):
    with open(img_path, 'rb')as read:
        b64 = base64.b64encode(read.read())
    return b64


url = 'http://127.0.0.1:8000/api/ocr'
img_b64 = img_to_base64('./img1.png')
res = requests.post(url=url, data={'img_b64': img_b64})

print(res.content.decode('utf-8'))
