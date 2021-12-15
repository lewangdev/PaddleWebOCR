import random
import base64
from io import BytesIO
from PIL import Image, ImageDraw

MAX_COMPRESS_SIZE = 1600


def compress_image(img: Image, compress_size: int) -> Image:
    if compress_size is None or compress_size <= 0:
        return img

    if img.height > MAX_COMPRESS_SIZE or img.width > MAX_COMPRESS_SIZE:
        scale = max(img.height / MAX_COMPRESS_SIZE, img.width / MAX_COMPRESS_SIZE)

        new_width = int(img.width / scale + 0.5)
        new_height = int(img.height / scale + 0.5)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return img


def rotate_image(img: Image) -> Image:
    if hasattr(img, '_getexif') and img._getexif() is not None:
        orientation = 274
        exif = dict(img._getexif().items())
        if orientation in exif:
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    return img


def draw_box_on_image(img: Image, texts: list) -> Image:
    img_draw = ImageDraw.Draw(img)
    colors = ['red', 'green', 'blue', "purple"]
    for line in texts:
        points = [tuple(point) for point in line[0]]
        points.append(points[0])
        # img_draw.polygon(points, outline=colors[random.randint(0, len(colors) - 1)])
        img_draw.line(points, width=4, fill=colors[random.randint(0, len(colors) - 1)])
    return img


def convert_image_to_bytes(img: Image) -> bytes:
    img_byte = BytesIO()
    img.save(img_byte, format='JPEG')
    return img_byte.getvalue()


def b64encode(bytes_data: bytes) -> str:
    return base64.b64encode(bytes_data).decode('utf8')


def convert_image_to_b64(img: Image) -> str:
    return b64encode(convert_image_to_bytes(img))


def convert_bytes_to_image(bytes_data: bytes) -> Image:
    return Image.open(BytesIO(bytes_data))


def convert_b64_to_image(b64_data: str) -> Image:
    return Image.open(BytesIO(base64.b64decode(b64_data.encode('utf8'))))
