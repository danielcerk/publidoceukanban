import os
import io
import tempfile
import zipfile
from PIL import Image
import subprocess
from pikepdf import Pdf
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_file(file, output_dir=None):

    if isinstance(file, InMemoryUploadedFile):

        filename = os.path.splitext(os.path.basename(file.name))[0]
        ext = os.path.splitext(file.name)[1].lower()

        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=ext)

        for chunk in file.chunks():

            temp_input.write(chunk)

        temp_input.flush()
        temp_input_path = temp_input.name
        temp_input.close()

        input_path = temp_input_path

    else:

        filename = os.path.splitext(os.path.basename(file))[0]

        ext = os.path.splitext(file)[1].lower()
        input_path = file

    if output_dir is None:

        output_dir = tempfile.gettempdir()

    if ext in [".jpg", ".jpeg", ".png", ".webp"]:

        image = Image.open(input_path)
        output_path = os.path.join(output_dir, f"{filename}{ext}")

        image.save(output_path, optimize=True, quality=75)

        return output_path

    elif ext in [".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".aac"]:

        output_path = os.path.join(output_dir, f"{filename}{ext}")

        subprocess.run([
            "ffmpeg", "-i", input_path,
            "-vcodec", "libx264",
            "-crf", "28",
            "-preset", "fast",
            "-acodec", "aac",
            output_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_path

    elif ext == ".pdf":

        output_path = os.path.join(output_dir, f"{filename}{ext}")

        with Pdf.open(input_path) as pdf:

            pdf.save(output_path, compression=Pdf.CompressionLevel.default)

        return output_path

    else:

        temp_zip = os.path.join(output_dir, f"{filename}.zip")

        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:

            zipf.write(input_path, arcname=os.path.basename(input_path))

        return temp_zip
