class Room:
    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name
    name = property(get_name, set_name)