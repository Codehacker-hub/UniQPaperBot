# UniQPaperBot 📚

UniQPaperBot is a Telegram bot designed to help students access previous-year question papers for various university programs such as BCA, BBA, and BCOM. This bot simplifies the process of retrieving subject-wise question papers by allowing students to select their stream, semester, and subject. With an easy-to-use interface, UniQPaperBot provides a seamless experience for academic resources.

## Features 🎓
- **Stream Selection**: Choose from multiple streams like BCA, BBA, and BCOM.
- **Semester Selection**: Get question papers for each semester.
- **Subject Selection**: Choose from a variety of subjects based on the selected stream and semester.
- **File Sharing**: Download the question papers directly through Telegram.
- **Author Information**: Learn more about the bot's creator and contact details.

## Requirements 📋
- Python 3.7+
- [Telegram Bot API](https://core.telegram.org/bots) token
- SQLite for database management
- Python libraries:
  - `python-telegram-bot`
  - `python-dotenv`
  - `sqlite3`

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/UniQPaperBot.git
   cd UniQPaperBot
2. **Set up the environment**: Install required Python libraries:
    ```bash
    pip install -r requirements.txt
3. **Create a .env file** and add your Telegram Bot token:
    ```bash
    TELEGRAM_BOT_TOKEN=your-bot-token-here
4. **Configure the Database**:
The bot uses an SQLite database (pdf_files.db) to store and retrieve question paper details. Populate the database with the appropriate data using the provided script       or manually as per your requirements.

5. **Run the Bot**:
   ```bash
   python bot.py
## Usage 🚀
Start the bot by typing /start in your Telegram chat.
Choose your stream, semester, and subject to receive the relevant previous-year question papers.
## Contributing 🤝
Fork the repository and create a new branch.
Submit pull requests with your improvements.
## Author 👤
Developed by: Ashutosh
Portfolio: Visit Portfolio
Contact: Telegram
## License 📄
This project is licensed under the MIT License.
   
### Key Points:
- Replace `your-username`, `your-bot-token-here`, `your-portfolio-link`, and `your-telegram-link` with the appropriate values.
- This markdown file will render well on GitHub with headings, lists, and links for easy navigation.

