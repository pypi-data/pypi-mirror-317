from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

def get_dpi(o):
    image = None
    if isinstance(o, str) or isinstance(o, Path):
        image = Image.open(str(o))
    if image is None:
        return None
    
    dpi = None
    exif_data = image._getexif()
    try:
        dpi = image.info['dpi']
    except:
        pass
        # if not exif_data:
        #     for k,v in exif_data.items():
        #         tag = TAGS.get(k)
        #         if tag in ('XResolution', 'YResolution'):
    return dpi
