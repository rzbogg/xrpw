import sys
import qrcode
from qrcode.image.styledpil import StyledPilImage

from wallet.store import DataBase

def qr_code_ascii(text:str):
    qr = qrcode.QRCode()
    qr.add_data(text)
    qr.print_ascii(out=sys.stdout)

def qr_code_image(text:str,db:DataBase | None = None):
    qr = qrcode.QRCode()
    qr.add_data(text)
    img = qr.make_image(image_factory=StyledPilImage)
    img.save('./test.png')


if __name__ == '__main__':
    qr_code_image('hello world',None)




