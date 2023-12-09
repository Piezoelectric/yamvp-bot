import pytesseract
from PIL import ImageGrab
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# char_whitelist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890: %@#~>"


# tesseract_config = '--psm 6'
tesseract_config = ''
bbox = (0, 290, 500, 470)
screenshot = ImageGrab.grab(bbox)
# screenshot.show()

capture_string = pytesseract.image_to_string(screenshot, config=tesseract_config)

clean_string = re.sub(r'\n(?!\[)', '', capture_string)

# print(capture_string)
# print("cleaned")

MVP_PATTERN = r"mvp"
CH_PATTERN = r"c[ch] *(\d{1,2})"
TIME_PATTERN = r"xx[: ]*(\d{2})"

for s in clean_string.splitlines():
    s = s.lower()
    print(s) # TODO: add debug flag for this

    # Find regex objects or None
    mvp = re.search(MVP_PATTERN, s)
    channel = re.search(CH_PATTERN, s)
    time = re.search(TIME_PATTERN, s)

    # TODO: Bound checking channel and time ints
    if mvp and channel and time:
        print("I found one!")

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