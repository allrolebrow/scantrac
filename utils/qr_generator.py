import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw
import os, uuid

def generate_qr(token: str, save_folder: str, base_url: str) -> str:
    """
    Generate a styled QR code image for a batch token.
    Returns the filename (relative path to static/qrcodes/).
    """
    scan_url = f"{base_url}/scan/{token}"
    filename = f"{token}.png"
    filepath = os.path.join(save_folder, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(scan_url)
    qr.make(fit=True)

    # Styled QR with rounded modules and brand color
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=(255, 255, 255),
            front_color=(10, 10, 15),   # dark brand color
        )
    ).convert("RGB")

    # Add accent dot in center
    size = img.size[0]
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = size // 12
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, 229, 160))  # accent green

    img.save(filepath)
    return filename
