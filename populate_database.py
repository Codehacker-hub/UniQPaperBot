import os
import sqlite3

def insert_file(stream, semester, subject, file_path, year):
    try:
        conn = sqlite3.connect('pdf_files.db')
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO files (stream, semester, subject_name, file_path, year)
            VALUES (?, ?, ?, ?, ?)
        ''', (stream, semester, subject, file_path, year))
        conn.commit()
        print(f"Inserted: {file_path}")  # Debugging print
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Define SUBJECTS and base_path here
# Dictionary of subjects by stream and semester
SUBJECTS = {
    "BCA": {
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
    },
    "BBA": {
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
    },
    "BCOM": {
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
    # Add other streams as needed
}

def populate_database():
    # Set the base path dynamically for deployment compatibility
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pdfs')
    
    for stream, semesters in SUBJECTS.items():
        for semester, subjects in semesters.items():
            # Construct the path for each semester folder
            semester_folder = os.path.join(base_path, stream, f"Sem_{semester.split()[-1]}")
            
            # Check if the folder exists before processing files
            if os.path.exists(semester_folder):
                for subject in subjects:
                    # Standardize subject code by replacing spaces with dashes
                    subject_code = subject.split(":")[0].replace(" ", "-")
                    subject_file_prefix = f"{stream}_Sem_{semester.split()[-1]}_{subject_code}"

                    # Iterate over files in the semester folder
                    for file_name in os.listdir(semester_folder):
                        if file_name.startswith(subject_file_prefix) and file_name.endswith(".pdf"):
                            file_path = os.path.join(semester_folder, file_name)
                            
                            # Extract the year from the filename
                            year_str = file_name.split("_")[-1].split(".pdf")[0]
                            try:
                                year = int(year_str)
                            except ValueError:
                                continue  # Skip if year is invalid

                            # Insert file details into the database
                            insert_file(stream, semester, subject, file_path, year)

populate_database()

