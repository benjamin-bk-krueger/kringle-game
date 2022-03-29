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
    def set_supportedby(self, supports):
        self.__supports = supports
    def get_supportedby(self):
        return self.__supports
    def set_requires(self, requires):
        self.__requires = requires
    def get_requires(self):
        return self.__requires
    
    
    difficulty = property(get_difficulty, set_difficulty)
    url = property(get_url, set_url)
    supportedby = property(get_supportedby, set_supportedby)
    requires = property(get_requires, set_requires)
