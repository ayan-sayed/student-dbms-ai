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

def main_menu():
    print('\n=== STUDENT DATABASE SYSTEM ===')
    print('1. Add Student')
    print('2. View all Students')
    print('3. Search Student')
    print('4. Delete Student')
    print('5. Update student')
    print('6. Ask AI')
    print('7. Exit')

def again(prompt):
    while True:
        answer = input(prompt).lower()
        if answer not in ['y', 'n']:
            print('Error! Please enter a valid choice!')
            continue
        return answer == 'n'          

def add_student(db):
    while True:
        student_id = input('Enter your unique ID: ').strip()
        if student_id in db:
            print('ID already exits! Try a different one.')
            continue

    
        name = input('Enter your name: ')

        try:
            age = float(input('Enter your age: '))
        except ValueError:
            print('Invalid age! Returning to main menu.')
            return
        
        course = input('Enter your course eg(BSC.IT): ')
        sem = input('Enter your semester: ')
        try:
            marks = float(input('Enter your CGPA (0-10): '))
        except ValueError:
            print('Invalid CGPA! Please enter a valid CGPA.')


        db[student_id] = {
            "name": name,
            "age": age, 
            "course": course,
            "sem": sem, 
            "marks": marks
        }
        print('Student Added successfully!')
            
        if again('Update another student (y/n)?: '):
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
    search_id = input('Enter the student ID: ').strip()
    if search_id in db: 
        d = db[search_id]
        row = [[search_id, d['name'], d['age'], d['course'], d['sem'], d['marks']]]
        headers = ['ID', 'Name', 'Age', 'Course', 'Sem', 'CGPA']
        print(tabulate(row, headers=headers, tablefmt='grid'))
    else: 
        print('No records found!')

def update_student(db):
    while True:
        update = input('Enter the student ID: ')
        if update not in db:
            print('ID not found! Please Enter a valid ID')
            continue
    

        print('-------------------------')
        print('1. Name')
        print('2. Age')
        print('3. Course')
        print('4. Sem')
        print('5. CGPA')
        print('6. All of the above')

        field_map = {
            1: ('name', 'Enter the updated name: ', str),
            2: ('age', 'Enter the updated age: ', float),
            3: ('course', 'Enter the updated course: ', str),
            4: ('sem', 'Enter the updated sem: ', str),
            5: ('marks', 'Enter the updated CGPA: ', float)
        }
        
        while True:
            choice = int(input('Enter the field you want to update eg(1,2,..): '))
            u = db[update]
            
            if choice in (1, 2, 3, 4, 5):
                    key, prompt, convert = field_map[choice]
                    new_value = convert(input(prompt))
                    u[key] = new_value

            elif choice == 6:
                for key, prompt, convert in field_map.items():
                    u[key] = convert(input(prompt))

            else:
                print('Please enter a valid field!')
                continue

            if again('Update another student (y/n)?: '):
                break

def delete_student(db):
    while True:
        delete_id = input('Enter the student ID: ').strip()
        if delete_id in db:
            del db[delete_id]
            print(f'Student ID {delete_id} was deleted successfully!')
        else: 
            print('No records found!') 

        if again('Delete another student (y/n)?: '):
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
        
        question = input('What would you like to ask? \n ->')
        data_text = json.dumps(db, indent=2)

        prompt = f"""Here is the student database data:
        {data_text}

        Answer this question based only on the data: {question}"""

        response = client.models.generate_content(
            model='gemini-2.5-flash' ,
            contents=prompt
        )

        print(f'\n {response.text} \n')

        if again('Ask another question (y/n)?: \n ->'):
            break

while True:
    main_menu()

    try:
        choice = int(input('Enter your choice: '))
    except ValueError:
        print('Error: Please enter a valid number!')
        continue
    
    if choice == 1:
        add_student(student)

    elif choice == 2:
        view_student(student)

    elif choice == 3:
        search_student(student)

    elif choice == 4:
        delete_student(student)

    elif choice == 5:
        update_student(student)

    elif choice == 6: 
        ask_ai(student)

    elif choice == 7: 
        save_data(student)
        break

    else:
        print('Invalid choice! Please enter a valid number')

    save_data(student)

    should_continue = ''
    while should_continue not in ['y', 'n']:
        should_continue = input('Want to perform other operations? (y/n): ').lower()
        if should_continue not in ['y', 'n']:
            print("Inavlid choice! Please enter 'y' or 'n'. ")

    if should_continue == 'n':
        print('Thank You!')
        break
