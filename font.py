import string

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np

FONT_NAME = ""
FONT_COLOURS = ["#000000", "#ff0000", "#a00041", "#ff9e1c", "#ffffff"]

font = ImageFont.truetype(f"fonts/{FONT_NAME}", 200)


def save_image(img: Image, letter: str, colour: str, height: int):
    height_percent = (height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    new_image = img.resize((width_size, height), Image.ANTIALIAS)
    new_image.save(f"output/{height}/{FONT_NAME.split('.')[0]}-{colour[1:]}-{letter}.png")


def get_image(letter: chr, colour: str):
    image = Image.new("RGBA", (500, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), letter, colour, font=font)
    ImageDraw.Draw(image)

    image_data = np.asarray(image)
    image_data_columns = image_data.max(axis=0, initial=0)
    image_data_rows = image_data.max(axis=1, initial=0)
    non_empty_columns = [col[3] for col in image_data_columns]
    non_empty_rows = [row[3] for row in image_data_rows]

    column_0 = next((i for i, x in enumerate(non_empty_columns) if x != 0), 0)
    column_1 = len(non_empty_columns) - next((i for i, x in enumerate(reversed(non_empty_columns)) if x != 0), -1)

    # row_0 = next((i for i, x in enumerate(non_empty_rows) if x != 0), 0)
    # row_1 = len(non_empty_rows) - next((i for i, x in enumerate(reversed(non_empty_rows)) if x != 0), -1)

    crop_box = (25, 275, column_0, column_1)

    image_data_new = image_data[crop_box[0]:crop_box[1]+1, crop_box[2]:crop_box[3]+1, :]
    new_image = Image.fromarray(image_data_new)

    for height in [25, 50, 100, 250]:
        save_image(img=new_image, letter=letter, colour=colour, height=height)


for c in string.ascii_letters + string.digits + "!-:.,+åÅöÖäÄøØæÆ%&()=;*€$<>":
    for colour in FONT_COLOURS:
        get_image(letter=c, colour=colour)
