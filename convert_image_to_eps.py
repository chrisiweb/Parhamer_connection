import os
from PIL import Image
from standard_dialog_windows import critical_window

def remove_transparency(im, bg_color=(255, 255, 255)):
    ### Taken from https://stackoverflow.com/a/35859141/7444782

    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        alpha = im.convert('RGBA').split()[-1]

        bg = Image.new("RGBA", im.size, bg_color + (255,))
        bg.paste(im, mask=alpha)
        return bg
    else:
        return im

def convert_image_to_eps(image):
    name, ext = os.path.splitext(image)

    try:
        fig = Image.open(image)

        if fig.mode in ('RGBA', 'LA'):
            # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=eps#eps
            # print('Current figure mode "{}" cannot be directly saved to .eps and should be converted (e.g. to "RGB")'.format(fig.mode))
            fig = remove_transparency(fig)
            fig = fig.convert('RGB')

        out_fig = str(name)+'.eps'
        fig.save(out_fig)
        fig.close()
        return True
    except Exception as e:
        return e


        



    ###https://stackoverflow.com/questions/47398291/saving-to-eps-not-supported-in-python-pillow
    # if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
    #     output = str(name) + ".eps"
    #     # output=all.replace('jpg','eps')
    #     img = Image.open(str(all))
    #     img.save(output)
    # elif ext.lower() == ".png":
    #     output = str(name) + ".eps"
    #     img = Image.open(str(all))
    #     img = img.convert("RGB")
    #     img.save(output)
    # else:
    #     warning_window(
    #         "Die Datei konnte nicht konvertiert werden."
    #     )
    #     return