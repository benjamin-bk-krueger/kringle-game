class Object:
    """
    Defines a generic object you can interact with
    """
    def __init__(self):
        self.__visited = False

    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name

    def set_visited(self, visited):
        self.__visited = visited
    def get_visited(self):
        return self.__visited

    def set_description(self, description):
        self.__description = description
    def get_description(self):
        return self.__description

    def set_location(self, location):
        self.__location = location
    def get_location(self):
        return self.__location
    
    name = property(get_name, set_name)
    visited = property(get_visited, set_visited)
    description = property(get_description, set_description)
    location = property(get_location, set_location)
