from enum import Enum, auto
from PIL import ImageTk, Image


class FruitsImagesType(Enum):
    APPLE = auto()
    BANANA = auto()
    ORANGE = auto()
    PINEAPPLE = auto()
    PEAR = auto()
    CHERRY = auto()
    STRAWBERRY = auto()
    KIWIFRUIT = auto()
    WATERMELON = auto()
    PEACH = auto()

    def get_image(type):

        if type == FruitsImagesType.APPLE:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/apple.gif"))

        if type == FruitsImagesType.BANANA:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/banana.gif"))

        if type == FruitsImagesType.ORANGE:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/orange.gif"))

        if type == FruitsImagesType.PINEAPPLE:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/pineapple.gif"))

        if type == FruitsImagesType.PEAR:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/pear.gif"))

        if type == FruitsImagesType.CHERRY:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/cherry.gif"))

        if type == FruitsImagesType.STRAWBERRY:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/strawberry.gif"))

        if type == FruitsImagesType.KIWIFRUIT:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/kiwifruit.gif"))

        if type == FruitsImagesType.WATERMELON:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/watermelon.gif"))

        if type == FruitsImagesType.PEACH:
            return ImageTk.PhotoImage(Image.open("Images/Fruits/peach.gif"))
