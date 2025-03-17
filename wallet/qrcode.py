import subprocess
import tempfile
import sys
import qrcode
from qrcode.image.styledpil import StyledPilImage


def qr_code_ascii(text:str):
    qr = qrcode.QRCode()
    qr.add_data(text)
    qr.print_ascii(out=sys.stdout)

def create_and_open_qrcode(text:str):
    qr = qrcode.QRCode()
    qr.add_data(text)
    img = qr.make_image(image_factory=StyledPilImage)
    with tempfile.NamedTemporaryFile() as file:
        img.save(file)
        _ = subprocess.run(
            ['feh', file.name]
        )



if __name__ == '__main__':
    create_and_open_qrcode('hello world')




