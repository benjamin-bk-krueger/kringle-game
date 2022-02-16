class Junction:
    """
    Defines a junction between two rooms
    """
    def set_destination(self, destination):
        self.__destination = destination
    def get_destination(self):
        return self.__coming_from

    def set_description(self, description):
        self.__description = description
    def get_description(self):
        return self.__description
    
    destination = property(get_destination, set_destination)
    description = property(get_description, set_description)