from Object import Object


class Objective(Object):
    """
    Defines an objective which you can achieve
    """
    def set_location(self, location):
        self.__location = location
    def get_location(self):
        return self.__location
    
    location = property(get_location, set_location)