class Room:
    """
    Defines a room which can hold further objects
    """
    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name
    def set_image(self, image):
        self.__image = image
    def get_image(self):
        return self.__image
    name = property(get_name, set_name)
    image = property(get_image, set_image)