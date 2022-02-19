import unittest
import game

class TestGame(unittest.TestCase):

    def test_load_data(self):
        self.assertGreater(game.load_data(), 0, "Loaded data should be greater than 0")

    def test_loaded_rooms(self):
        self.assertGreater(len(game.rooms), 0, "Loaded rooms should be greater than 0")
    
    def test_loaded_objectives(self):
        self.assertGreater(len(game.objectives), 0, "Loaded objectives should be greater than 0")

    def test_loaded_junctions(self):
        self.assertGreater(len(game.junctions), 0, "Loaded junctions should be greater than 0")
    
    def test_display_image(self):
        self.assertTrue(game.display_image("logo"), "Display image logo is not successful")

if __name__ == '__main__':
    unittest.main()