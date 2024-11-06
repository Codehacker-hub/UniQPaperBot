import os
import logging
import sqlite3
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def log_user_info(update: Update) -> None:
    user = update.effective_user
    chat = update.effective_chat

    logging.info(
        f"User Info: ID: {user.id}, Username: {user.username}, First Name: {user.first_name}, Last Name: {user.last_name}, Chat ID: {chat.id}"
    )

# Configure logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    # format='%(asctime)s - %(message)s'
)

logged_users = set()

def log_user_request(user_id, user_name, request):
    logging.info(f"User ID: {user_id}, User Name: {user_name}, Request: {request}")

# logger = logging.getLogger(__name__)

# List of available streams (adjust according to your needs)
AVAILABLE_STREAMS = ["BCA", "BBA", "BCOM"]

# Dictionary to hold subjects for each semester of BCA
BCA_SUBJECTS = {
   "Semester 1": [
        "BCA-16-101: English (Compulsory) - A",
        "BCA-16-102: Fundamentals of Mathematical Statistics",
        "BCA-16-103: Computer Fundamentals and Computing Software",
        "BCA-16-104: Problem Solving through C"
    ],
    "Semester 2": [
        "BCA-16-201: English (Compulsory) - B",
        "BCA-16-202: Computer Organization",
        "BCA-16-203: Fundamentals of Web Programming",
        "BCA-16-204: Object Oriented Programming using C++"
    ],
    "Semester 3": [
        "BCA-16-301: Punjabi - A",
        "BCA-16-302: History and Culture of Punjab - A",
        "BCA-16-303: Information System Design and Implementation",
        "BCA-16-304: Computer Oriented Numerical Methods",
        "BCA-16-305: Data Structures"
    ],
    "Semester 4": [
        "BCA-16-401: Punjabi - B",
        "BCA-16-402: History and Culture of Punjab - B",
        "BCA-16-403: Software Project Management",
        "BCA-16-404: Operating System Concepts and Linux",
        "BCA-16-405: Database Management System"
    ],
    "Semester 5": [
        "BCA-16-501: Computer Networks",
        "BCA-16-502: Discrete Mathematical Structure",
        "BCA-16-503: Java Programming",
        "BCA-16-504: Web Application using PHP"
    ],
    "Semester 6": [
        "BCA-16-601: E-commerce",
        "BCA-16-602: Application Development using VB.Net",
        "BCA-16-603: Computer Graphics and Multimedia Applications"
    ]
}

# Dictionary to hold subjects for each semester of BBA
BBA_SUBJECTS = {
    "Semester 1": [
        "BBA 101A: Punjabi",
        "BBA 101B: History and Culture of Punjab",
        "BBA 102: Organisation Behaviour",
        "BBA 103: Fundamentals of Information Technology",
        "BBA 104: Management Concepts and Practices",
        "BBA 105: Financial Accounting",
        "BBA 106: Essentials of Business Economics – I"
    ],
    "Semester 2": [
        "BBA 121A: Punjabi",
        "BBA 121B: History and Culture of Punjab",
        "BBA 122: Business Statistics",
        "BBA 123: Essentials of Business Economics – II",
        "BBA 124: Legal Aspects of Business",
        "BBA 125: Personality Development & Professional Skills",
        "BBA 126: Managerial Accounting"
    ],
    "Semester 3": [
        "BBA 201: English & Business Communication Skills",
        "BBA 202: Operation Research",
        "BBA 203: Marketing Management",
        "BBA 204: Economics of Money and Banking",
        "BBA 205: Legal Framework for Companies",
        "BBA 206: Tax Laws - I"
    ],
    "Semester 4": [
        "BBA 221: English & Business Communication Skills",
        "BBA 222: Financial Management",
        "BBA 223: Research Methodology",
        "BBA 224: Human Resource Management",
        "BBA 225: Tax Laws - II",
        "BBA 226: Fundamentals of E-Commerce"
    ],
    "Semester 5": [
        "BBA 301: Principles of Insurance and Risk Management",
        "BBA 302: Financial Markets and Financial Services",
        "BBA 303: Business Environment",
        "BBA 304: Entrepreneurship and New Venture Creation",
        "BBA 305: Consumer Behaviour",
        "BBA 306: Sales and Logistics Management",
        "BBA 307: Financial Statement Analysis",
        "BBA 308: Investment Management",
        "BBA 309: Organizational Development",
        "BBA 310: Industrial Relations and Labour Legislation"
    ],
    "Semester 6": [
        "BBA 321: Business Policy and Strategy",
        "BBA 322: Production and Operations Management",
        "BBA 323: Business Ethics and Corporate Governance",
        "BBA 325: Advertising and Brand Management",
        "BBA 326: Retail Management",
        "BBA 327: Cost Accounting and Analysis",
        "BBA 328: Strategic Financial Management",
        "BBA 329: Human Resource Planning and Performance Management",
        "BBA 330: Compensation Management"
    ]
}

# Dictionary tp hold subjects for each semester of BCOM
BCOM_SUBJECTS = {
    "Semester 1": [
        "BCM 101 A: Punjabi",
        "BCM 101 B: History and Culture of Punjab",
        "BCM 102: English and Business Communication",
        "BCM 103: Interdisciplinary Psychology for Managers",
        "BCM 104: Business Economics-I",
        "BCM 105: Principles of Financial Accounting",
        "BCM 106: Commercial Laws",
        "BCM 107: Principles and Practices of Management"
    ],
    "Semester 2": [
        "BCM 201 A: Punjabi",
        "BCM 201 B: History and Culture of Punjab",
        "BCM 202: English and Business Communication",
        "BCM 203: Interdisciplinary E-Commerce",
        "BCM 204: Business Economics-II",
        "BCM 205: Corporate Accounting",
        "BCM 206: Business Laws",
        "BCM 207: Human Resource Management"
    ],
    "Semester 3": [
        "BCM 301: Interdisciplinary Issues in Indian Commerce",
        "BCM 302: Cost Accounting",
        "BCM 303: Company Law",
        "BCM 304: Business Mathematics and Statistics",
        "BCM 305: Banking and Insurance",
        "BCM 306: Goods and Services Tax (GST)"
    ],
    "Semester 4": [
        "BCM 401: Interdisciplinary Security Analysis and Portfolio Management",
        "BCM 402: Advanced Accounting",
        "BCM 403: Auditing and Secretarial Practice",
        "BCM 404: Cost Management",
        "BCM 405: Marketing Management",
        "BCM 406: Quantitative Techniques and Methods"
    ],
    "Semester 5": [
        "BCM 501: Income Tax Law",
        "BCM 502: Management Accounting",
        "BCM 503: Indian Economy",
        "BCM 504: Production and Operation Management",
        "BCM 505: Entrepreneurship and Small Business",
        "BCM 506: Financial Markets and Services"
    ],
    "Semester 6": [
        "BCM 601: Direct Tax Laws",
        "BCM 602: Financial Management",
        "BCM 603: Issues in Financial Reporting",
        "BCM 604: Social and Business Ethics",
        "BCM 605: Operational Research",
        "BCM 606: Sectoral Aspects of Indian Economy"
    ]
}

# BABSC_SUBJECTS = {
# }

STREAM_SUBJECTS = {"BCA": BCA_SUBJECTS, "BBA": BBA_SUBJECTS, "BCOM": BCOM_SUBJECTS}

# Function to get subject names for a given stream and semester from the database
def fetch_subjects(stream, semester):
    conn = sqlite3.connect('pdf_files.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT subject_name FROM pdf_files
        WHERE stream = ? AND semester = ?
    ''', (stream, semester))
    subjects = cursor.fetchall()
    conn.close()
    return [subject[0] for subject in subjects]

# Function to get PDF file paths from the database for stream, semester, and subject
def fetch_files(stream, semester, subject):
    conn = sqlite3.connect('pdf_files.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT file_path FROM pdf_files
        WHERE stream = ? AND semester = ? AND subject_name = ?
    ''', (stream, semester, subject))
    files = cursor.fetchall()
    conn.close()
    return [file[0] for file in files]

# Start command: Asks for stream selection
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    user_id = user.id
    first_name = user.first_name
    user_name = update.effective_user.username or update.effective_user.first_name 
    request = "Started the bot"

    log_identifier = (user_id, request)

    if log_identifier not in logged_users:
        logging.info(f"User ID: {user_id}, User Name: {user_name}, First Name: {first_name}, Request: {request}")
        logged_users.add(log_identifier)


    # Display available streams to the user
    keyboard_buttons = [[stream] for stream in AVAILABLE_STREAMS]
    reply_keyboard = ReplyKeyboardMarkup(keyboard_buttons, one_time_keyboard=True, resize_keyboard=True, selective=True)


    await update.message.reply_text(
        "🌟 Welcome to the DAV PYQ Bot! Please choose your stream: 🌟",
        reply_markup=reply_keyboard
    )
    log_user_request(user_id, user_name, "Started the bot")

# Author info handler for the "About the Author" button

# Handle stream selection
async def handle_stream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name
    selected_stream = update.message.text  # The text of the button clicked

    log_user_request(user_id, user_name, f"Selected stream: {selected_stream}")

    stream = update.message.text
    context.user_data["stream"] = stream
    if stream in STREAM_SUBJECTS:
        semesters = list(STREAM_SUBJECTS[stream].keys())
        await update.message.reply_text(
            "Please select your semester:",
            reply_markup=ReplyKeyboardMarkup([[semester] for semester in semesters], one_time_keyboard=True)
        )
        return "semester"
    else:
        await update.message.reply_text("Question Paper not available for selected stream right now!!")
        return "stream"

# Handle semester selection
async def handle_semester(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = update.effective_user.id
    user_name = update.effective_user.username or update.effective_user.first_name
    selected_semester = update.message.text  # The text of the button clicked

    log_user_request(user_id, user_name, f"Selected Semester: {selected_semester}")

    semester = update.message.text
    stream = context.user_data["stream"]
    context.user_data["semester"] = semester
    if semester in STREAM_SUBJECTS[stream]:
        subjects = STREAM_SUBJECTS[stream][semester]
        await update.message.reply_text(
            "Please select your subject:",
            reply_markup=ReplyKeyboardMarkup([[subject] for subject in subjects], one_time_keyboard=True)
        )
        return "subject"
    else:
        await update.message.reply_text("Invalid semester. Please try again.")
        return "semester"

# Handle subject selection and send files
async def handle_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    subject = update.message.text
    stream = context.user_data["stream"]
    semester = context.user_data["semester"]

    # Connect to the database
    conn = sqlite3.connect("pdf_files.db")
    cursor = conn.cursor()
    
    # Fetch the files based on stream, semester, and subject
    cursor.execute(
        "SELECT file_path FROM files WHERE stream = ? AND semester = ? AND subject_name = ?",
        (stream, semester, subject)
    )
    files = cursor.fetchall()
    conn.close()
    
    if files:
        await update.message.reply_text("Sending available question paper files.....")
        for file_path, in files:
            await update.message.reply_document(open(file_path, 'rb'))
    else:
        await update.message.reply_text("Sorry, no files found for your selection.")
    return "stream"  # Go back to stream selection after sending the files


# Main function to start the bot
def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^({"|".join(AVAILABLE_STREAMS)})$'), handle_stream))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^Semester \d$'), handle_semester))
    application.add_handler(MessageHandler(filters.TEXT, handle_subject))
    
    application.run_polling()

if __name__ == '__main__':
    main()
