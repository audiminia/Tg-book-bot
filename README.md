# Tg-book-bot
A Telegram bot that provides books using the Libgen and its API.

## Features

- book search: people can search for by name or author name and get detailed information about the book, including release date, publishers, book format available.
- provide book in ebook format like pdf, epub.

## How to Use

1. Start the bot by searching for "@TheGameInfoBot" on Telegram or by clicking [here](https://t.me/TheGameIntoBot).
2. Use the following commands to interact with the bot:
   - `/start`: Displays a welcome message and provides basic information about the bot.
   - `/help`: Provides a list of available commands and their usage instructions.
   - `/book <book name>`: retrieve book name and provide you related output.

## Development

To set up the development environment and run the bot locally, follow these steps:

1. Clone the repository:
```git clone https://github.com/your-username/tg-book-bot.git```

2. Install the required dependencies:
```
cd tg-book-bot
pip install -r requirements.txt
```

3. Create a new Telegram bot and obtain the bot token.

4. Set up the environment variables:
- Create a `.env` file in the project root directory.
- Add the following environment variables to the file:
  ```
  API_ID=your_telegram_api_id
  API_HASH=your_telegram_api_hash
  BOT_TOKEN=your_telegram_bot_token
  ```

5. Run the bot:
```
python bot.py
```

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
