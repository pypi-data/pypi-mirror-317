import unittest
from qb_bot.api import QBBotAPI

class TestQBBotAPI(unittest.TestCase):
    def test_send_question(self):
        bot = QBBotAPI()
        response = bot.send_question("Hello, what is your name?")
        self.assertIsInstance(response, str)  # Check if the response is a string

if __name__ == "__main__":
    unittest.main()
