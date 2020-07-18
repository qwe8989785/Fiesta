import qrcode
from flask import send_file
from io import BytesIO
def _serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png', cache_timeout=0)

def enQRcode(inputData):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    qr.add_data(inputData)
    qr.make(fit=True)
    img = qr.make_image()
    return img

