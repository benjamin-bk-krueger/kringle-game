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
    
    difficulty = property(get_difficulty, set_difficulty)
    url = property(get_url, set_url)