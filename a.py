import pytesseract
from PIL import ImageGrab, ImageEnhance
import re, time

class MvpBot:

    def __init__(self):
        # TODO: use dotenv
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # tesseract_config = '--psm 6'
        self.tesseract_config = ''
        self.BBOX = (0, 290, 500, 470)

        self.MVP_PATTERN = r"mvp"
        self.CH_PATTERN = r"c[ch] *(\d{1,2})"
        self.TIME_PATTERN = r"xx[: ]*(\d{2})"

        self.delay = 5

    def capture(self):
        screenshot = ImageGrab.grab(self.BBOX)
        desaturate = ImageEnhance.Color(screenshot)
        screenshot = desaturate.enhance(0.0)
        contrast = ImageEnhance.Contrast(screenshot)
        screenshot = contrast.enhance(2.0)
        self.capture_string = pytesseract.image_to_string(screenshot, config=self.tesseract_config)
        
    def clean_and_parse(self):
        clean_string = re.sub(r'\n(?!\[)', '', self.capture_string)

        for s in clean_string.splitlines():
            s = s.lower()
            print(s) 

            # Find regex objects or None
            mvp = re.search(self.MVP_PATTERN, s)
            channel = re.search(self.CH_PATTERN, s)
            time = re.search(self.TIME_PATTERN, s)

            # TODO: Bound checking channel and time ints
            if mvp and channel and time:
                print("I found one!")

    def run(self):
        while True:
            self.capture()
            self.clean_and_parse()
            time.sleep(self.delay)

if __name__ == '__main__':
    b = MvpBot()
    b.run()

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