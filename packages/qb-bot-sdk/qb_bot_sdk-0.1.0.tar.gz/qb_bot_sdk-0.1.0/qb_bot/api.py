import requests

class QBBotAPI:
    BASE_URL = "http://127.0.0.1:8000/qb_bot_api/"  # Replace with your actual API URL

    def __init__(self):
        self.session = requests.Session()
        self.conversation_history = []

    def send_question(self, question):
        """Send a question to the bot and return the response."""
        try:
            payload = {"question": question}
            response = self.session.post(self.BASE_URL, data=payload)
            response.raise_for_status()
            data = response.json()
            self.conversation_history.append(f"User: {question}")
            self.conversation_history.append(f"Bot: {data.get('answer')}")
            return data.get("answer")
        except requests.exceptions.RequestException as e:
            raise QBBotAPIError(f"An error occurred: {e}")

class QBBotAPIError(Exception):
    """Custom exception for errors in the QBBotAPI."""
    pass
