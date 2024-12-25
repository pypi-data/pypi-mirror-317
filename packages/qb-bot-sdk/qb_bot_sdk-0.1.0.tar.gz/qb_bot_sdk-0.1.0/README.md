# QB Bot SDK

A Python SDK to interact with the QB Bot API.

## Installation
```bash
pip install qb-bot-sdk





## Installation
from qb_bot.api import QBBotAPI

bot = QBBotAPI()
response = bot.send_question("Hello, what is your name?")
print(response)