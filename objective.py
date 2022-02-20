from object import Object

class Objective(Object):
    """
    Defines an objective you can achieve
    """
    def set_difficulty(self, difficulty):
        self.__difficulty = difficulty
    def get_difficulty(self):
        return self.__difficulty
    def set_url(self, url):
        self.__url = url
    def get_url(self):
        return self.__url
    def set_supports(self, supports):
        self.__supports = supports
    def get_supports(self):
        return self.__supports
    
    difficulty = property(get_difficulty, set_difficulty)
    url = property(get_url, set_url)
    supports = property(get_supports, set_supports)
