import pytesseract
from PIL import ImageGrab, ImageEnhance
import re

class ImageParser:
    def __init__(self, tesseract_filepath, bb):
        # screenshot and OCR config
        pytesseract.pytesseract.tesseract_cmd = rf'{tesseract_filepath}'
        # tesseract_config = '--psm 6'
        self.tesseract_config = ''
        self.BBOX = bb

        # regex/parse config
        self.MVP_PATTERN = r"mvp"
        self.CH_PATTERN = r"c[ch] *(\d{1,2})"
        # TODO: revise to include "channel", limit ch range
        self.TIME_PATTERN = r"xx[: ]*(\d{2})"
        # revise to limit time range (no impossible hours)
        # maybe also revise logic: MVP and (CH or Time) 

    def capture(self):
        screenshot = ImageGrab.grab(self.BBOX)
        desaturate = ImageEnhance.Color(screenshot)
        screenshot = desaturate.enhance(0.0)
        contrast = ImageEnhance.Contrast(screenshot)
        screenshot = contrast.enhance(2.0)
        self.capture_string = pytesseract.image_to_string(screenshot, config=self.tesseract_config)
        
    def clean_and_parse(self):
        clean_string = re.sub(r'\n(?!\[)', '', self.capture_string)
        output = []

        for s in clean_string.splitlines():
            s = s.lower()
            # print(s) 

            # Find regex objects or None
            mvp = re.search(self.MVP_PATTERN, s)
            channel = re.search(self.CH_PATTERN, s)
            time = re.search(self.TIME_PATTERN, s)

            # TODO: Bound checking channel and time ints
            if mvp and channel and time:
                output.append(s)

        return output

# notes to self
# bot process
# main
# * capture
# * distinguish beg from actual post
# * post to discord

# healthcheck process (separate process?)
# health determined by most recent msg (captured by bot? or sent to discord?)
# could be both

# * check if MS down (via taskman? unsure)
# * check if bot down 
#     (healthcheck: when did it write a txt msg)
# * check if discord integration down (bot alive, can't post)
#     (healthcheck: when was the bot's last msg in the discord channel)