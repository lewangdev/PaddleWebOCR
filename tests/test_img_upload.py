import requests
url = 'http://127.0.0.1:8000/api/ocr'
img1_file = {
    'img_upload': open('img1.png', 'rb')
}
res = requests.post(url=url, data={'compress': 0}, files=img1_file)

print(res.content.decode('utf-8'))
