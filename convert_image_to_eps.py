import os
from PIL import Image


def remove_transparency(im, bg_color=(255, 255, 255)):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        alpha = im.convert("RGBA").split()[-1]

        bg = Image.new("RGBA", im.size, bg_color + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im

    ### Taken from https://stackoverflow.com/a/35859141/7444782


def convert_image_to_eps(image, quality_index):
    name, ext = os.path.splitext(image)

    try:
        fig = Image.open(image)

        if fig.mode in ("RGBA", "LA", "P", "PA"):
            fig = remove_transparency(fig)
            fig = fig.convert("RGB")

        out_fig = str(name) + ".eps"
        if quality_index == 0:
            quality = (400,400)
        elif quality_index == 1:
            quality = (500,500)
        elif quality_index == 2:
            quality = (700,700)

        if quality_index != 3:
            fig.thumbnail(quality)
        fig.save(out_fig)
        fig.close()
        return True
    except Exception as e:
        return e

    ### https://stackoverflow.com/questions/47398291/saving-to-eps-not-supported-in-python-pillow
