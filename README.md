# Student Database Management System (CLI)

A command-line interface (CLI) application for managing student records, featuring an integrated AI query assistant to answer questions about the stored data.

## Features

- **Add** — Insert a new student record into the database.
- **View** — Display all student records currently stored in the system.
- **Search** — Locate a specific student record using a defined search parameter.
- **Update** — Modify the details of an existing student record.
- **Delete** — Remove a student record from the database.
- **AI Assistant** — Query the student database using natural language, powered by the Gemini API.
- **Exit** — Close the application safely.

## Tech Stack

- Python
- tabulate
- google-genai
- python-dotenv
- JSON (for data storage)

## Prerequisites

Before running this application, ensure the following are available:

- Python installed on your system.
- A Gemini API key.

**Note:** A Gemini API key can be obtained free of charge through [Google AI Studio](https://aistudio.google.com/).

## Installation / Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ayan-sayed/student-dbms.git
   ```

2. Install the required dependencies:
   ```bash
   pip install tabulate google-genai python-dotenv
   ```

3. Create a `.env` file in the root directory of the project and add your Gemini API key and model name:
   ```
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

## How to Run

Execute the following command in your terminal:

```bash
python student_DBMS.py
```

## How to Use / Sample Menu

Upon running the application, the following interactive menu will be displayed:

```
 ================================
 |   STUDENT DATABASE SYSTEM    |
 ================================
[1]. Add Student
[2]. View all Students
[3]. Search Student
[4]. Update Student
[5]. Delete Student
[6]. Ask AI
[7]. Exit
 ================================
Select an option (1-7):
```

Users select an option by entering the corresponding number, and the system responds with prompts relevant to the chosen action. For most operations (Add, Search, Update, Delete, AI Assistant), the system will ask whether to perform the same action again before returning to the main menu.

## Project Structure

- `student_DBMS.py` — The main application script containing all program logic, menu handling, and CLI interactions.
- `database.json` — The local data file used to store student records in JSON format.
- `.env` — A user-created file used to store the Gemini API key and model name. This file is not included in the repository and must be created manually during setup.

## Future Improvements

- [ ] Replace JSON-based storage with a relational database
- [ ] Refactor the application into a modular architecture
- [ ] Enhance the AI assistant to query and analyze student data

## Author / Credits

- **Author:** Ayan Sayed
- **GitHub:** [https://github.com/ayan-sayed](https://github.com/ayan-sayed)
