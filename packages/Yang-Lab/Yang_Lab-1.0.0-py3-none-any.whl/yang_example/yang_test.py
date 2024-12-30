from loguru import logger

class YangTest:
    def __init__(self):
        self.default_text = "Passion!!"

    def printer(self, text=""):
        if text == "":
            text = self.default_text
        print(text)
        logger.info(text)
        pass