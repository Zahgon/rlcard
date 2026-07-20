
from PIL import Image, ImageDraw, ImageFilter


def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):  # FIXME: not used
    pass


ImageDraw.rounded_rectangle = rounded_rectangle  # FIXME: not used


def mask_rounded_rectangle_transparent(pil_img, corner_radius=8):  # FIXME: not used
    pass
