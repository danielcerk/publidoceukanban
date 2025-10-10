from PIL import Image
import io


def compress_image(file, format='JPEG', quality=85):
    image = Image.open(file)
    buffer = io.BytesIO()
    image.save(buffer, format=format, optimize=True, quality=quality)
    buffer.seek(0)
    return buffer
