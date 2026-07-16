import json
from tabulate import tabulate
import os
from dotenv import load_dotenv
from google import genai


try: 
    with open('database.json', 'r') as file:
        student = json.load(file)
except FileNotFoundError:
    student = {}
except json.JSONDecodeError as e:
    print(f'Warning: databse.json is corrupted or invalid ({e}).')
    print('Fix the file before running the program again.')
    exit(1)

def main_menu():
    print(' ================================')
    print(' |   STUDENT DATABASE SYSTEM    |')
    print(' ================================')
    print('[1]. Add Student')
    print('[2]. View all Students')
    print('[3]. Search Student')
    print('[4]. Delete Student')
    print('[5]. Update student')
    print('[6]. Ask AI')
    print('[7]. Exit')
    print(' ================================')

def again(prompt):
    while True:
        answer = input(F'{prompt} (y/n): ').strip().lower()
        if answer not in ['y', 'n']:
            print('Error: Please enter a valid choice!')
            continue
        return answer == 'n'          

def add_student(db):
    while True:
        student_id = input('Enter your unique ID: ').strip()
        if not student_id:
            print('Error: ID cannot be empty!')
            continue
        elif student_id in db:
            print('Error: ID already exits!')
            continue

    
        name = input('Enter your name: ').strip()

        while True:
            try:
                age = float(input('Enter your age: '))
                break
            except ValueError:
                print('Error: Please enter a valid number for age! ')
                

        course = input('Enter your course eg(BSC.IT): ').strip()
        sem = input('Enter your semester: ').strip()

        while True:
            try:
                marks = float(input('Enter your CGPA (0-10): '))
                if 0 <=marks <= 10:
                    break
                print('Error: CGPA must be between 0 and 10! ')
            except ValueError:
                print('Error: Please enter a valid decimal number!')


        db[student_id] = {
            "name": name,
            "age": age, 
            "course": course,
            "sem": sem, 
            "marks": marks
        }
        
        print('Student Added successfully!')
            
        if again('\nAdd another student?'):
            break

def view_student(db):
    if db == {}:
        print('No records found!')
        return
    
    rows = []

    for student_id, details in db.items():
        row = [student_id, details['name'], details['age'], details['course'], details['sem'], details['marks']]
        rows.append(row)

    headers = ['ID', 'Name', 'Age', 'Course', 'Sem', 'CGPA']
    print(tabulate(rows, headers=headers, tablefmt='grid'))

def search_student(db):
    if not db:
        print('No records found!')
        return
    
    while True:
        search_id = input('Enter the student ID: ').strip()
        if search_id in db: 
            d = db[search_id]
            row = [[search_id, d['name'], d['age'], d['course'], d['sem'], d['marks']]]
            headers = ['ID', 'Name', 'Age', 'Course', 'Sem', 'CGPA']
            print(tabulate(row, headers=headers, tablefmt='grid'))
        else: 
            print('No records found!')

        if again('\nSearch another student?'):
            break

def update_student(db):
    if not db:
        print('No records found!')
        return
    
    field_map = {
        1: ('name', 'Enter the updated name: ', str),
        2: ('age', 'Enter the updated age: ', float),
        3: ('course', 'Enter the updated course: ', str),
        4: ('sem', 'Enter the updated sem: ', str),
        5: ('marks', 'Enter the updated CGPA: ', float)
    }


    while True:
        update = input('Enter the student ID: ')
        if update not in db:
            print('ID not found! Please Enter a valid ID')
            continue

        u = db[update]

        print('-------------------------')
        print('1. Name\n2. Age\n3. Course\n4. Sem\n5. CGPA\n6. All Fields')
        print('-------------------------')
        

        
        while True:
            try:
                choice = int(input('Enter the field you want to update eg(1,2,..): '))
            except ValueError:
                print('Error: Enter a valid number!')
            
            if choice in (1, 2, 3, 4, 5):
                    key, prompt, convert = field_map[choice]
                    while True:
                        try:
                            u[key] = convert(input(prompt))
                            break
                        except ValueError:
                            print('Error: Invalid format!')
                    print('Field updated successfully!')

            elif choice == 6:
                for _, (key, prompt, convert) in field_map.items():
                    while True:
                        try:
                            u[key] = convert(input(prompt))
                            break
                        except ValueError:
                            print("Error: Invalid formmat. Please try again!")
                print('All fields updated successfully!')
            
            else:
                print('Please enter a valid field!')
                continue
            
            break
        
        if again('\nUpdate another student?'):
            break

def delete_student(db):
    while True:
        delete_id = input('Enter the student ID: ').strip()
        if delete_id in db:
            del db[delete_id]
            print(f'Student ID {delete_id} was deleted successfully!')
        else: 
            print('No records found!') 

        if again('\nDelete another student?'):
            break

def save_data(db):
    with open('database.json', 'w') as file:
        json.dump(db, file, indent=4)

def ask_ai(db):
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    while True:
        if not db:
            print('No record found!')
            return
        
        question = input('What would you like to ask? \n >')
        if not question:
            continue

        data_text = json.dumps(db, indent=2)
        prompt = f"""Here is the student database data:
        {data_text}

        Answer this question based only on the data: {question}"""

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash' ,
                contents=prompt
            )
            print(f'\n {response.text} \n')
        except Exception as e:
            print(f'AI Error: {e}')

        if again('Ask another question?'):
            break

WRITE_ACTIONS = {
    1 : add_student,
    4 : delete_student,
    5 : update_student
}
READ_ACTIONS = {
    2 : view_student,
    3 : search_student,
    6 : ask_ai
}

def handle_write(ch, db):
    WRITE_ACTIONS[ch](db)
    save_data(student)

def handle_read(ch, db):
    READ_ACTIONS[ch](student)
    
while True:
    main_menu()

    try:
        choice = int(input('Select an option (1-7): '))
    except ValueError:
        print('Error: Please enter a valid number!')
        continue

    if choice == 7: 
        save_data(student)
        print('Data saved. Goodbye!')
        break
    elif choice in WRITE_ACTIONS:
        handle_write(choice, student)
    elif choice in READ_ACTIONS:
        handle_read(choice, student)
    else:
        print('Error: Select an option between 1 and 7.')

    should_continue = ''
    while should_continue not in ['y', 'n']:
        should_continue = input('Perform other operations? (y/n): ').lower()
        if should_continue not in ['y', 'n']:
            print("Error: Enter 'y' or 'n'. ")

    if should_continue == 'n':
        print('Data saved. Goodbye!')
        break
