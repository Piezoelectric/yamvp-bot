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
        self.MVP_PATTERN = r"(mvp|alicia.*bless)"
        self.CH_PATTERN = r"c[ch]?(an)?(nel)?[ \.]*\d{1,2}"
        # hopefully this should account for c, cc, ch, chan, and channel.
        self.TIME_PATTERN = r"xx[: ]*(\d{1,2})"

        self.LOCATION_PATTERN = r"(shrine|mush|ms|hene|lith|leafre)"
        # optional: location of the MVP pop

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
            print(s) 

            # Find regex objects or None
            mvp = re.search(self.MVP_PATTERN, s)
            channel = re.search(self.CH_PATTERN, s)
            time = re.search(self.TIME_PATTERN, s)
            location = re.search(self.LOCATION_PATTERN, s)

            # TODO: Bound checking channel and time ints
            if mvp and (channel or time):
                #output.append([s, mvp, channel, time])
                output.append({
                    'msg': s,
                    'channel': channel.group(0) if channel else "couldn't parse",
                    'time': time.group(0) if time else "couldn't parse",
                    'location': location.group(0) if location else ''
                })

        return output
