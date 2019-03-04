from model.constants import WIDTH, HEIGHT
class Sky:
    """
    this class contains info about basic sky layer
    attributes: __w, __h
    methods:  getSize()
    """
    def __init__(self, width = WIDTH, height = HEIGHT):
        self.__w = width
        self.__h = height
    def getSize(self):
        return {"width": self.__w, "height":self.__h}
