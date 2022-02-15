class Object:
    """
    Defines a generic object you can interact with
    """
    def __init__(self):
        self.__visited = False

    def set_visited(self, visited):
        self.__visited = visited
    def get_visited(self):
        return self.__visited

    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name

    def set_description(self, description):
        self.__description = description
    def get_description(self):
        return self.__description

    def set_image(self, image):
        self.__image = image
    def get_image(self):
        return self.__image
    
    visited = property(get_visited, set_visited)
    name = property(get_name, set_name)
    description = property(get_description, set_description)
    image = property(get_image, set_image)